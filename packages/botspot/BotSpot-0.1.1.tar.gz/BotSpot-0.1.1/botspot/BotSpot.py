"""
    A module to find the botness of users from a twitter json dump.
"""

import json
import pandas as pd
import pickle as pk
import numpy as np
from .utils import *
from .featureLists import *
import traceback
import collections
from xgboost.sklearn import XGBClassifier
import xgboost as xgb
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class BotSpot:
    def __init__(self):
        self.user_feature_list = user_feature_list
        self.tweet_feature_list = tweet_feature_list
        self.word2vecEmbeddings =  None
        self.dataHashtags = None

    def setWord2VecEmbeddings(self, embeddings=None, embeddingsPath=None, forceReload=True):
        if not forceReload and self.word2vecEmbeddings is not None:
            return
        if embeddings is not None and embeddingsPath is not None:
            raise Exception("Please only specify one source for the Word2Vec embeddings.")
        elif embeddings is not None and isinstance(embeddings, collections.Mapping):
            self.word2vecEmbeddings = embeddings
        elif embeddingsPath is not None:
            _,fileextension = os.path.splitext(embeddingsPath)
            if fileextension == '.pickle':
                print("Loading Word2Vec Embeddings...")
                with open(embeddingsPath,"rb") as f:
                    self.word2vecEmbeddings = pk.load(f)
                print("Finished loading Word2Vec Embeddings")
            elif fileextension == '.txt':
                print("Loading Word2Vec Embeddings...")
                with open(embeddingsPath,"r") as f:
                    model = {}
                    for line in f:
                        splitLine = line.split()
                        word = splitLine[0]
                        embedding = np.array([float(val) for val in splitLine[1:]])
                        model[word] = embedding
                    self.word2vecEmbeddings = model
                print("Finished loading Word2Vec Embeddings")
    
    def extractTweets(self, filePath, tweetLimit = None, embeddings=None, embeddingsPath=None, hashtagFilter=None):
        """Extracts tweets from a json dump into a pandas dataframe"""
        # Appending DataFrames line by line is inefficient, because it generates a
        # new dataframe each time. It better to get the entire list and them concat.
        user_list = []
        tweet_list = []
        w2v_content_list = []
        w2v_description_list = []
        with open(filePath) as f:
            for i, line in enumerate(f,1):
                if tweetLimit is not None and tweetLimit < i:
                    break
                j = json.loads(line)
                try:
                    temp_user = {}
                    temp_tweet = {}
                    temp_content = {'status_text':j['text'], 'user_id' : j['user']['id']}
                    temp_description = {'description':j['user']['description'], 'user_id' : j['user']['id']}
                    
                    temp_user['user_id'] = j['user']['id']
                    temp_tweet['user_id'] = j['user']['id']

                    temp_user.update(getTextFeatures('name',j['user']['name']))
                    temp_user.update(getTextFeatures('location',j['user']['location']))
                    temp_user.update(getTextFeatures('description',j['user']['description']))
                    for key in ['statuses_count', 'listed_count', 'friends_count', 'followers_count']:
                        temp_user[key] = j['user'][key]
                    temp_user['verified'] = 1 if j['user']['verified'] else 0
                    temp_user['ff_ratio'] = (temp_user['followers_count'] + 1)/(temp_user['followers_count'] + temp_user['friends_count'] + 1)
                    temp_user['years_on_twitter'] = (datetime.now() - datetime.strptime(j['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')).days/365
                    temp_user['statuses_rate'] = (temp_user['statuses_count'] + 1)/(temp_user['years_on_twitter'] + .001)
                    temp_user['tweets_to_followers'] = (temp_user['statuses_count'] + 1)/(temp_user['followers_count'] + 1)
                    temp_user['retweet_count'] = j['retweet_count']
                    temp_user['favorite_count'] = j['favorite_count']
                    temp_user['favourites_count'] = j['user']['favourites_count']

                    temp_tweet.update(getTextFeatures('status_text',j['text']))
                    temp_tweet['n_tweets'] = 1 if 'retweeted_status' in j and ('quoted_status_is' in j) else 0
                    temp_tweet['n_retweets'] = 1 if 'retweeted_status' in j else 0
                    temp_tweet['n_quotes'] = 1 if 'quoted_status_id' in j else 0
                    temp_tweet['n_timeofday'] = hourofweekday(j['created_at'])
                    temp_tweet.update(getSource(j['source']))

                    user_list.append(temp_user)
                    tweet_list.append(temp_tweet)
                    w2v_content_list.append(temp_content)
                    w2v_description_list.append(temp_description)
                except Exception as err:
                    traceback.print_tb(err.__traceback__)
        # We are assuming that user data doesn't change much and if it does, we take that 'latest' as our feature
        userDataframe = pd.DataFrame(user_list).fillna(0).set_index('user_id')
        userDataframe = userDataframe[~userDataframe.index.duplicated(keep='last')]
        
        tweetDataframe = pd.DataFrame(tweet_list).fillna(0).set_index('user_id')
        n_retweets = tweetDataframe['n_retweets'].groupby('user_id').sum()
        n_quoted = tweetDataframe['n_quotes'].groupby('user_id').sum()
        tweetDataframe = tweetDataframe.groupby('user_id').mean()
        tweetDataframe['n_retweets'] = n_retweets
        tweetDataframe['n_quotes'] = n_quoted

        # We need to filter out the features we don't have in our training set
        userDataframe = userDataframe[self.user_feature_list]
        tweetDataframe = tweetDataframe[self.tweet_feature_list]

        contentDataframe = pd.DataFrame(w2v_content_list).set_index('user_id')
        descriptionDataframe = pd.DataFrame(w2v_description_list).set_index('user_id')
        descriptionDataframe = descriptionDataframe[~descriptionDataframe.index.duplicated(keep='last')]
        
        if embeddingsPath is not None or embeddings is not None:
            self.setWord2VecEmbeddings(embeddings,embeddingsPath, forceReload=False)
            w2vDataframe = self.__computeVectors(contentDataframe, descriptionDataframe)
        self.featureDataframe = userDataframe.join(tweetDataframe)
        if self.word2vecEmbeddings is not None:
            self.featureDataframe = self.featureDataframe.join(w2vDataframe)
        if hashtagFilter is not None:
            self.dataHashtags = hashtagFilter
            hashtagdf = self.__computeHashtagFeatures(contentDataframe)[hashtagFilter]
            self.featureDataframe = self.featureDataframe.join(hashtagdf)
        return self.featureDataframe

    def __computeHashtagFeatures(self, contentdf):
        hashtagSeries = contentdf['status_text'].str.findall(r'(?<!\w)#\w+').str.join(" ").str.replace("#","")
        userIndex = hashtagSeries.index
        crop = hashtagSeries.tolist()
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(crop)
        transformer = TfidfTransformer(smooth_idf=False)
        tfidf = transformer.fit_transform(X)
        column_names = vectorizer.get_feature_names()
        hashtagdf = pd.DataFrame(tfidf.toarray(), columns=column_names, index=userIndex)
        return hashtagdf

    def __computeVectors(self, contentdf, descriptiondf):
        ud = {}
        for index,row in contentdf.iterrows():
            vec = np.zeros(300)
            tol = 0
            for w in parse(row['status_text']):
                if w in self.word2vecEmbeddings:
                    vec = vec + np.array(self.word2vecEmbeddings[w])
                    tol += 1
            vec = vec/tol
            if index in ud:
                ud[index].append(vec)
            else:
                ud[index] = [vec]
        for k,v in ud.items():
            ud[k] = np.array(v).mean(axis=0)
        conw2v = pd.DataFrame(ud)
        conw2v = conw2v.T
        conw2v.index.name = 'user_id'
        conw2v.columns = ["con_w2v_" + str(i) for i in conw2v.columns]
        
        ud = {}
        for index,row in descriptiondf.iterrows():
            vec = np.zeros(300)
            tol = 0
            for w in parse(row['description']):
                if w in self.word2vecEmbeddings:
                    vec = vec + np.array(self.word2vecEmbeddings[w])
                    tol += 1
            if tol != 0:
                vec = vec/tol
            ud[index] = [vec]
        for k,v in ud.items():
            ud[k] = np.array(v).mean(axis=0)
        desw2v = pd.DataFrame(ud)
        desw2v = desw2v.T
        desw2v.index.name = 'user_id'
        desw2v.columns = ["des_w2v_" + str(i) for i in desw2v.columns]

        return conw2v.join(desw2v)
    
    def loadClassifierModel(self, fname):
        clf = XGBClassifier(
        learning_rate =0.1,
        n_estimators=80,
        max_depth=5, #16
        subsample=0.6,
        colsample_bytree=1,
        objective= 'binary:logistic',
        n_jobs=10,
        silent=True,
        seed =27
        )
        clf.load_model(fname)
        self.clf = clf

    def trainClassifierModel(self, labelledDataPath, saveFileName=None):
        params = {
        'learning_rate' :0.1,
        'n_estimators':80,
        'max_depth':5, #16
        'subsample':0.6,
        'colsample_bytree':1,
        'objective': 'binary:logistic',
        'n_jobs':10,
        'silent':True,
        'seed' :27
        }

        _,fileextension = os.path.splitext(labelledDataPath)
        if fileextension == '.csv':
            botrnot = pd.read_csv(labelledDataPath, sep ="\t")
        elif fileextension == '.pickle':
            with open(labelledDataPath,'rb') as f:
                botrnot = pk.load(f)
        if 'is_bot' in botrnot.columns:
            print(botrnot.columns)
            botTarget = botrnot['is_bot']
        elif 'isbot' in botrnot.columns:
            botTarget = botrnot['isbot']
        else:
            raise Exception("Neither an is_bot or isbot column was found in the data. Please label your target column accordingly.")
        # Get hashtag which need removing i.e. those is aren't in our training data
        if self.dataHashtags is not None:
            hashtagsToRemove = list(set(self.dataHashtags) - set(botrnot.columns)) #Note that this is liable to error if a hashtag has the same value as a feature column.
            self.featureDataframe.drop(hashtagsToRemove)
        if len(set(self.featureDataframe.columns.values) - set(botrnot.columns.values)) > 0:
            # We want to check that all the features we requested are in the training set
            raise Exception("There are some features in the training set which are missing, namely ",set(self.featureDataframe.columns.values) - set(botrnot.columns.values))
        botrnot = botrnot[self.featureDataframe.columns.values]
        train = xgb.DMatrix(botrnot.values, botTarget.values, feature_names=botrnot.columns.values)
        self.clf = xgb.train(params, train, 80)
        if saveFileName is not None:
            self.clf.save_model(saveFileName)

    def getBotness(self):
        if self.clf is None:
            raise Exception("The classifier has not been loaded yet")
        if self.featureDataframe is None:
            raise Exception("Tweets haven't been extracted yet")
        test = xgb.DMatrix(self.featureDataframe.values, feature_names=self.featureDataframe.columns.values)
        bdf = pd.DataFrame()
        bdf['botness'] = self.clf.predict(test)
        bdf['user_id'] = self.featureDataframe.index
        self.botnessDataframe = bdf.set_index('user_id')
        return self.botnessDataframe



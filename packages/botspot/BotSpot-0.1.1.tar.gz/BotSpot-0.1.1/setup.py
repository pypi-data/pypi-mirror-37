# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['botspot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'botspot',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Rohit Ram',
    'author_email': 'rohit.ram@anu.edu.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

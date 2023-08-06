# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zhlib']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'cjkradlib>=0.1.2,<0.2.0',
 'jieba>=0.39.0,<0.40.0',
 'peewee>=3.7,<4.0',
 'requests>=2.20,<3.0',
 'wordfreq>=2.2,<3.0']

setup_kwargs = {
    'name': 'zhlib',
    'version': '0.1.0',
    'description': 'Dictionaries and what to learn in Chinese',
    'long_description': None,
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

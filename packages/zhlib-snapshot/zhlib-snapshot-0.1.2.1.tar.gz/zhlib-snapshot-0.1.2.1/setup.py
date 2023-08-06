# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zhlib_snapshot']

package_data = \
{'': ['*']}

install_requires = \
['jieba>=0.39.0,<0.40.0',
 'peewee>=3.7,<4.0',
 'regex==2018.02.21',
 'wordfreq>=2.2,<3.0']

setup_kwargs = {
    'name': 'zhlib-snapshot',
    'version': '0.1.2.1',
    'description': 'Snapshot of zhlib: Dictionaries and what to learn in Chinese',
    'long_description': None,
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

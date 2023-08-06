# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ttslib']

package_data = \
{'': ['*']}

install_requires = \
['google_speech>=1.0,<2.0',
 'gtts>=2.0,<3.0',
 'importlib_resources>=1.0,<2.0',
 'ruamel.yaml>=0.15.74,<0.16.0']

setup_kwargs = {
    'name': 'ttslib',
    'version': '0.1.0.1',
    'description': 'TTS for both online and local usage that works',
    'long_description': None,
    'author': 'patarapolw',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

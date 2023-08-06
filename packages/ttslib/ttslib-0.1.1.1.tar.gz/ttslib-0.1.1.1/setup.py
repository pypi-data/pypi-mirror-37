# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ttslib', 'ttslib.data']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0',
 'pyttsx3>=2.7,<3.0',
 'ruamel.yaml>=0.15.74,<0.16.0']

setup_kwargs = {
    'name': 'ttslib',
    'version': '0.1.1.1',
    'description': "TTS for local usage that works for all OS's, with a simple interface",
    'long_description': None,
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

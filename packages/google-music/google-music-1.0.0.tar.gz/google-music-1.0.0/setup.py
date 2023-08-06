# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['google_music', 'google_music.clients']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'audio-metadata>=0.1,<0.2',
 'google-music-proto>=1.0,<2.0',
 'protobuf>=3.5,<4.0',
 'requests-oauthlib>=1.0,<2.0',
 'tenacity>=5.0,<6.0']

extras_require = \
{'dev': ['flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0.0,<2.0.0',
         'sphinx>=1.7,<2.0'],
 'doc': ['sphinx>=1.7,<2.0'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'google-music',
    'version': '1.0.0',
    'description': 'A Google Music API wrapper.',
    'long_description': '\n',
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'url': 'https://github.com/thebigmunch/google-music',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

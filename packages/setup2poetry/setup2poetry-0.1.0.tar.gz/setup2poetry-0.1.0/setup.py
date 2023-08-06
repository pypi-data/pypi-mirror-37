# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['setup2poetry']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['setup2poetry = setup2poetry.cli:main']}

setup_kwargs = {
    'name': 'setup2poetry',
    'version': '0.1.0',
    'description': 'Tool to convert setup.py to poetry pyproject.toml',
    'long_description': None,
    'author': 'Matt Magin',
    'author_email': 'matt.magin@cmv.com.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

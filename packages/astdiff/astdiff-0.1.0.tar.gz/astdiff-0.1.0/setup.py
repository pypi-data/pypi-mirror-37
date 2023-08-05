# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['astdiff']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0',
 'colorful>=0.4.1,<0.5.0',
 'six>=1.11,<2.0',
 'typing>=3.6,<4.0']

entry_points = \
{'console_scripts': ['astdiff = astdiff:astdiff.astdiff']}

setup_kwargs = {
    'name': 'astdiff',
    'version': '0.1.0',
    'description': 'Ensure the invariance of the Abstract Syntax Tree across commits.',
    'long_description': None,
    'author': 'Walter Moreira',
    'author_email': 'wmoreira@auntbertha.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

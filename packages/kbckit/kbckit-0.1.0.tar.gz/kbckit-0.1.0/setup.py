# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kbckit']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'logzero>=1.5,<2.0',
 'pandas>=0.23.4,<0.24.0',
 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'kbckit',
    'version': '0.1.0',
    'description': 'Toolkit for KBC',
    'long_description': None,
    'author': 'Ryo Takahashi',
    'author_email': 'reiyw.setuve@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

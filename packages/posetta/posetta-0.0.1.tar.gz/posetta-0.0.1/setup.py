# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['posetta',
 'posetta.data',
 'posetta.gui',
 'posetta.lib',
 'posetta.readers',
 'posetta.writers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'fastkml>=0.11.0,<0.12.0',
 'lxml>=4.2,<5.0',
 'pandas>=0.23.4,<0.24.0']

setup_kwargs = {
    'name': 'posetta',
    'version': '0.0.1',
    'description': 'The universal translator of geodetic coordinate file formats',
    'long_description': None,
    'author': 'Geir Arne Hjelle',
    'author_email': 'geir.arne.hjelle@kartverket.no',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

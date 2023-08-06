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
['click>=7.0', 'fastkml>=0.11.0', 'lxml>=4.2', 'pandas>=0.23.0']

entry_points = \
{'console_scripts': ['posetta = posetta.__main__:cli',
                     'posetta_gui = posetta.__main__:gui']}

setup_kwargs = {
    'name': 'posetta',
    'version': '0.0.3',
    'description': 'The Universal Translator of Geodetic Coordinate File Formats',
    'long_description': '# Posetta, the Universal Translator of Geodetic Coordinate File Formats\n\nPosetta is a command line and GUI utility for translating between different\nfile formats used for representing geodetic coordinates.\n\n**Note:** Posetta is still in pre-alpha status. Its functionality will change,\n  and it should not be depended on in any production-like setting.\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n## Installing Posetta\n\nPosetta is available at [PyPI](https://pypi.org/project/posetta/). You can\ninstall it by simply running\n\n    pip install posetta\n\n\n## Installing Posetta from source\n\nPosetta depends on other brilliant Python packages, like for instance numpy. We\nrecommend using the Anaconda distribution to ease the installation of these\ndependencies.\n\n### Install Anaconda\n\nGo to [www.anaconda.com/download](https://www.anaconda.com/download), and\ndownload Anaconda for Python 3.\n\n\n### Download the Posetta source code\n\nIf you have not already done so, download the Posetta source code, from\n[GitHub](https://github.com/NordicGeodesy/posetta). Then enter the main\n`posetta` directory before running the install commands below.\n\n    cd posetta\n\n\n### Install dependencies\n\nYou should now install the necessary dependencies using the\n`environment.yml`-file. You can do this either in your current conda\nenvironment, or choose to create a new `posetta`-environment. In general, you\nshould install `posetta` in its own environment.\n\nTo install `posetta` in a new environment named `posetta` and activate it, do\n\n    conda env create -n posetta -f environment.yml\n    conda activate posetta\n\nTo instead install `posetta` in your current environment, do\n\n    conda env update -f environment.yml\n\n\n### Install the Posetta package\n\nTo do the actual installation of Posetta, use the `flit` packaging tool:\n\n    flit install --dep production\n\nIf you want to develop the Posetta package, install it in editable mode using\n\n    flit install -s\n\nOn Windows, you can install in editable mode using\n\n    flit install --pth-file\n\n\n## Using Posetta\n\nPosetta can be used either as a command line application, or a graphical (GUI)\napplication.\n\n\n### Posetta at the command line\n\nYou can use Posetta as a command line tool. Run the following to see instructions:\n\n    posetta --help\n\n\n### Posetta as a graphical (GUI) application\n\nPosetta can also be used as a simple point and click GUI application. Run the\nfollowing command to start it:\n\n    posetta_gui\n\n\n',
    'author': 'Nordic Geodetic Commision',
    'author_email': 'geir.arne.hjelle@kartverket.no',
    'url': 'https://github.com/NordicGeodesy/posetta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

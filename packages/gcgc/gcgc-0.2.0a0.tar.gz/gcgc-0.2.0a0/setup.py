# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gcgc',
 'gcgc.alphabet',
 'gcgc.encoded_seq',
 'gcgc.tests',
 'gcgc.tests.alphabet',
 'gcgc.tests.cli',
 'gcgc.tests.encoded_seq',
 'gcgc.tests.fixtures']

package_data = \
{'': ['*'], 'gcgc.tests.fixtures': ['p53_human/*']}

install_requires = \
['biopython==1.72', 'numpy==1.15.2']

entry_points = \
{'console_scripts': ['gcgc = gcgc.cli:main']}

setup_kwargs = {
    'name': 'gcgc',
    'version': '0.2.0a0',
    'description': '',
    'long_description': None,
    'author': 'Trent Hauck',
    'author_email': 'trent@trenthauck.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

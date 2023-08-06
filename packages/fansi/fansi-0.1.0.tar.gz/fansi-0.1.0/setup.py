# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fansi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fansi',
    'version': '0.1.0',
    'description': 'A Python library that makes formatting terminal printouts easy.',
    'long_description': '# Fansi\nFansi is a python library that makes formatting terminal printouts easy.\n',
    'author': 'Daniel Rivas Perez',
    'author_email': 'drivas12@googlemail.com',
    'url': 'https://github.com/drivasperez/fansi/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)

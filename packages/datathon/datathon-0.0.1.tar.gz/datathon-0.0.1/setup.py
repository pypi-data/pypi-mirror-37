# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['datathon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datathon',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'datathon-authors',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

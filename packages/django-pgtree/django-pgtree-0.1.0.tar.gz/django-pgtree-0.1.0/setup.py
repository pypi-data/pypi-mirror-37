# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_pgtree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-pgtree',
    'version': '0.1.0',
    'description': 'Heirachial data for Django with Postgres.',
    'long_description': None,
    'author': 'Adam Brenecki',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)

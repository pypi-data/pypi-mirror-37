# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pgnotify']

package_data = \
{'': ['*']}

install_requires = \
['logx', 'psycopg2-binary']

setup_kwargs = {
    'name': 'pgnotify',
    'version': '0.1.1539662717',
    'description': '',
    'long_description': None,
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

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
    'version': '0.1.1539665961',
    'description': 'Easily LISTEN to PostgreSQL NOTIFY notifications',
    'long_description': "# pgnotify: Easily LISTEN to PostgreSQL NOTIFY notifications\n\nLISTEN to and process NOTIFY events with a simple for loop, like so:\n\n    from pgnotify import await_pg_notifications\n\n    for notification in await_pg_notifications(\n            'postgresql:///nameofdatabase',\n            ['nameoflisteningchannel', 'nameoflisteningchannel2']):\n\n        print(notification.channel)\n        print(notification.payload)\n\nMore docs to come.\n",
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'url': 'https://github.com/djrobstep/pgnotify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

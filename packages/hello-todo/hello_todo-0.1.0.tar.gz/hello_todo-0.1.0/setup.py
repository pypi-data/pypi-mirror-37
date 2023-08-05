# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hello_todo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'hello-todo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mathias Ngo',
    'author_email': 'gogs@fake.local',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

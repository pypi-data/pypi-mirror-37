# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hello_todo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['todos = hello_todo.cli:hello']}

setup_kwargs = {
    'name': 'hello-todo',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Mathias Ngo',
    'author_email': 'ngo.mathias@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

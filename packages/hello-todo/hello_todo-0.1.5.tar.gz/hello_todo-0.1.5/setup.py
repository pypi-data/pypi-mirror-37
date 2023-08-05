# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hello_todo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['add_todo = hello_todo.cli:add_todo',
                     'add_todolist = hello_todo.cli:add_todolist',
                     'init_todos = hello_todo.cli:init_todo',
                     'todolist = hello_todo.cli:todo_list',
                     'todos = hello_todo.cli:todo_lists']}

setup_kwargs = {
    'name': 'hello-todo',
    'version': '0.1.5',
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

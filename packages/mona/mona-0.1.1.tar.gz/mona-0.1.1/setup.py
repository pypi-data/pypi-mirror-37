# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mona',
 'mona.cli',
 'mona.hashing',
 'mona.plugins',
 'mona.rules',
 'mona.sci',
 'mona.sci.aims']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.6,<4.0']

extras_require = \
{'cli': ['toml>=0.9.6,<0.10.0', 'click>=7.0,<8.0'],
 'cov': ['coverage>=4.5,<5.0'],
 'doc': ['sphinx>=1.8,<2.0',
         'toml>=0.9.6,<0.10.0',
         'sphinxcontrib-asyncio>=0.2.0,<0.3.0',
         'sphinx-autodoc-typehints>=1.3,<2.0'],
 'graphviz': ['graphviz>=0.10.0,<0.11.0'],
 'sci': ['numpy>=1.15,<2.0', 'textx>=1.5,<1.6'],
 'test': ['pytest>=3.8,<4.0', 'pytest-mock>=1.10,<2.0']}

entry_points = \
{'console_scripts': ['mona = mona.cli:cli.main']}

setup_kwargs = {
    'name': 'mona',
    'version': '0.1.1',
    'description': 'Calculation framework',
    'long_description': '# Mona\n\n[![build](https://img.shields.io/travis/azag0/mona/master.svg)](https://travis-ci.org/azag0/mona)\n[![coverage](https://img.shields.io/codecov/c/github/azag0/mona.svg)](https://codecov.io/gh/azag0/mona)\n![python](https://img.shields.io/pypi/pyversions/mona.svg)\n[![pypi](https://img.shields.io/pypi/v/mona.svg)](https://pypi.org/project/mona/)\n[![commits since](https://img.shields.io/github/commits-since/azag0/mona/latest.svg)](https://github.com/azag0/mona/releases)\n[![last commit](https://img.shields.io/github/last-commit/azag0/mona.svg)](https://github.com/azag0/mona/commits/master)\n[![license](https://img.shields.io/github/license/azag0/mona.svg)](https://github.com/azag0/mona/blob/master/LICENSE)\n[![code style](https://img.shields.io/badge/code%20style-black-202020.svg)](https://github.com/ambv/black)\n\nMona is a calculation framework that turns normal execution of Python functions into a graph of tasks. Each task is hashed by the code of its function and by its inputs, and the result of each executed task is cached. The cache can be stored persistently in an SQLite database. Tasks can be executed in parallel within a single Mona instance, and multiple instances can work in parallel on the same database.\n\n## Installing\n\nInstall and update using [Pip](https://pip.pypa.io/en/stable/quickstart/).\n\n```\npip install -U mona\n```\n\n## Links\n\n- Documentation: https://azag0.github.io/mona\n\n## A simple example\n\n```python\nfrom mona import Rule, Session\n\n@Rule\nasync def total(xs):\n    return sum(xs)\n\n@Rule\nasync def fib(n):\n    if n < 2:\n        return n\n    return total([fib(n - 1), fib(n - 2)])\n\nwith Session() as sess:\n    sess.eval(fib(5))\n    dot = sess.dot_graph()\ndot.render(view=True)\n```\n\n![](https://raw.githubusercontent.com/azag0/mona/master/docs/fib.gv.svg?sanitize=true)\n\n',
    'author': 'Jan Hermann',
    'author_email': 'dev@janhermann.cz',
    'url': 'https://github.com/azag0/mona',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fresh_baked_skeleton']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0', 'typing>=3.6,<4.0']

entry_points = \
{'console_scripts': ['fresh_baked_skeleton = fresh_baked_skeleton.cli:cli']}

setup_kwargs = {
    'name': 'fresh-baked-skeleton',
    'version': '0.1.0a124',
    'description': 'Short Description of My Library',
    'long_description': '# Fresh Baked Skeleton\n\n[![Build Status](https://travis-ci.org/Curly-Mo/fresh-baked-skeleton.svg?branch=master)](https://travis-ci.org/Curly-Mo/fresh-baked-skeleton)\n[![Coverage](https://coveralls.io/repos/github/Curly-Mo/fresh-baked-skeleton/badge.svg)](https://coveralls.io/github/Curly-Mo/fresh-baked-skeleton)\n[![Documentation](https://readthedocs.org/projects/fresh-baked-skeleton/badge/?version=latest)](https://fresh-baked-skeleton.readthedocs.org/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/fresh-baked-skeleton.svg)](https://pypi.python.org/pypi/fresh-baked-skeleton)\n[![PyPI Pythons](https://img.shields.io/pypi/pyversions/fresh-baked-skeleton.svg)](https://pypi.python.org/pypi/fresh-baked-skeleton)\n[![License](https://img.shields.io/pypi/l/fresh-baked-skeleton.svg)](https://github.com/Curly-Mo/fresh-baked-skeleton/blob/master/LICENSE)\n\nShort Description of My Library\n\n## Features\n\n* What it do?\n\n## Usage\n\n* TODO\n\n## Install\n\n```console\npip install fresh-baked-skeleton\n```\n\n## Documentation\nSee https://fresh-baked-skeleton.readthedocs.org/en/latest/\n\n## Development\n```console\npip install poetry\ncd fresh-baked-skeleton\npoetry install\n```\n### Run\nTo run cli entrypoint:\n```console\npoetry run fresh_baked_skeleton --help\n```\n\n### Tests\n```console\npoetry run tox\n```\n\n### Docker\nTo run with docker\n```console\ndocker build -t Fresh Baked Skeleton .\ndocker run fresh_baked_skeleton:latest fresh_baked_skeleton --help\n```\n',
    'author': 'Colin Fahy',
    'author_email': 'colin@cfahy.com',
    'url': 'https://github.com/Curly-Mo/fresh-baked-skeleton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

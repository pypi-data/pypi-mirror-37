# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon_manager']

package_data = \
{'': ['*']}

install_requires = \
['toml']

entry_points = \
{'console_scripts': ['dophon_manager = dophon_manager:main']}

setup_kwargs = {
    'name': 'dophon-manager',
    'version': '0.1.2.post1',
    'description': '',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

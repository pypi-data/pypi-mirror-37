# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pcte_dynaprov', 'pcte_dynaprov.services']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0',
 'aiohttp>=3.4,<4.0',
 'click>=7.0,<8.0',
 'jsonschema>=2.6,<3.0',
 'pika>=0.12.0,<0.13.0',
 'pyvmomi>=6.7,<7.0']

entry_points = \
{'console_scripts': ['pcte-dynamic-provision = main:cli']}

setup_kwargs = {
    'name': 'pcte-dynamic-provisioning',
    'version': '0.1.0',
    'description': 'Dynamic Provisioning of the PCTE Greyspace Environment',
    'long_description': '',
    'author': 'Jordan Gregory',
    'author_email': 'jordan.gregory@metova.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

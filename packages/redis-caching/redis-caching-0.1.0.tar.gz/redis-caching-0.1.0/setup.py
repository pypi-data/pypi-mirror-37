# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['redis_caching']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.1,<2.0', 'dill>=0.2.8,<0.3.0']

setup_kwargs = {
    'name': 'redis-caching',
    'version': '0.1.0',
    'description': 'A Python library for caching in Redis',
    'long_description': '# redis-caching\nPython library for caching in Redis\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'url': 'https://github.com/rominf/redis-caching',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['speed_stack']

package_data = \
{'': ['*']}

extras_require = \
{'dill': ['dill>=0.2.8,<0.3.0'],
 'multiprocess': ['dill>=0.2.8,<0.3.0', 'multiprocess>=0.70.6,<0.71.0'],
 'rapidjson': ['python-rapidjson>=0.6.3,<0.7.0'],
 'ujson': ['ujson>=1.35,<2.0']}

setup_kwargs = {
    'name': 'speed-stack',
    'version': '0.1.0',
    'description': 'This simplifies easy enhancements to python.',
    'long_description': '',
    'author': 'austinv11',
    'author_email': 'austinv11@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

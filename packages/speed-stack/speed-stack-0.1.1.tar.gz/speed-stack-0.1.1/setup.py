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
 'recommended': ['ujson>=1.35,<2.0',
                 'dill>=0.2.8,<0.3.0',
                 'multiprocess>=0.70.6,<0.71.0'],
 'recommended:sys_platform == "!windows"': ['uvloop>=0.11.2,<0.12.0'],
 'ujson': ['ujson>=1.35,<2.0'],
 'uvloop:sys_platform == "!windows"': ['uvloop>=0.11.2,<0.12.0']}

setup_kwargs = {
    'name': 'speed-stack',
    'version': '0.1.1',
    'description': 'This simplifies easy enhancements to python.',
    'long_description': '# Speed-Stack\nEasy enhancements to python by replacing system modules with various (optional)\nthird party packages.\n\nCurrent available configurations:\n* uvloop: Injects uvloop as the current asyncio EventLoop Policy\n* ujson: Injects ujson as the json module implementation\n* rapidjson: Injects python-rapidjson as the json module implementation\n* dill: Injects dill as the json module implementation\n* multiprocess: (Inherits the dill configuration) Injects multiprocess as the multiprocessing module implementation\n* recommended: Injects uvloop, ujson, dill and multiprocess.',
    'author': 'austinv11',
    'author_email': 'austinv11@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

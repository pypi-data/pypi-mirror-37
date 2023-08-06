# Speed-Stack
Easy enhancements to python by replacing system modules with various (optional)
third party packages.

Current available configurations:
* uvloop: Injects uvloop as the current asyncio EventLoop Policy
* ujson: Injects ujson as the json module implementation
* rapidjson: Injects python-rapidjson as the json module implementation
* dill: Injects dill as the json module implementation
* multiprocess: (Inherits the dill configuration) Injects multiprocess as the multiprocessing module implementation
* recommended: Injects uvloop, ujson, dill and multiprocess.
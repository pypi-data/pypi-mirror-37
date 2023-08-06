__version__ = '0.1.0'


def _replace(replacement: str, target: str) -> bool:
    try:
        import sys
        if target in sys.modules:
            del sys.modules[target]
        sys.modules[target] = __import__(replacement)
        return True
    except:
        return False


def _hook():
    try:
        import uvloop
        import asyncio
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except:
        pass

    if not _replace("ujson", "json"):
        _replace("rapidjson", "json")
    _replace("dill", "pickle")


try:
    _hook()
except:
    pass

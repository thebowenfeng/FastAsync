import sys
from .exceptions.setup_exceptions import *
from .types.tasks import AsyncTask

version = sys.version_info
if version[0] < 3 or version[1] < 7:
    raise PythonVersionError("", version)

try:
    import threading
    import queue
except ImportError as e:
    raise RequiredModuleNotFoundError(e.name)


def make_async(func):
    def inner(*args, **kwargs):
        task = AsyncTask(func, *args, **kwargs)
        task.run()
        return task
    return inner

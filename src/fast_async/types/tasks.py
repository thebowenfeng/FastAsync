from typing import Callable
from threading import Thread
from ..exceptions.task_exceptions import AsyncTaskException


class AsyncTask:
    def __init__(self, func: Callable, *args, **kwargs):
        self.func: Callable = func
        self.args = args
        self.kwargs = kwargs
        self.status = 'pending'
        self.result = None
        self.thread: Thread = None
        self.exception: Exception = None

    def func_handler(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.status = 'success'
            self.result = result
        except Exception as e:
            self.exception = e
            self.status = 'failure'

    def run(self):
        child_thread = Thread(target=self.func_handler)
        self.thread = child_thread
        child_thread.start()

    def wait(self):
        self.thread.join()
        if self.exception is not None:
            raise AsyncTaskException(str(self.exception), self.func.__name__)

        return self.result

from typing import Callable
from threading import Thread
from ..exceptions.task_exceptions import AsyncTaskException
from queue import Queue


DEFAULT_MAX_THREADS = 64


class AsyncTask:
    def __init__(self, func: Callable, *args, **kwargs):
        self.func: Callable = func
        self.args = args
        self.kwargs = kwargs
        self.status = 'pending'
        self.result = None
        self.thread: Thread = None
        self.exception: Exception = None
        self.on_success = None
        self.on_error = None
        self.execute_on_caller = False

    def func_handler(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.status = 'success'
            self.result = result
            if self.on_success is not None and not self.execute_on_caller:
                self.on_success(self.result)
        except Exception as e:
            self.exception = e
            self.status = 'failure'
            if self.on_error is not None and not self.execute_on_caller:
                self.on_error(self.exception)

        global_task_manager.remove(self.thread)

    def run(self):
        child_thread = Thread(target=self.func_handler)
        self.thread = child_thread
        global_task_manager.put(child_thread)

    def wait(self):
        while not self.thread.is_alive():
            pass
        self.thread.join()
        if self.exception is not None:
            raise AsyncTaskException(str(self.exception), self.func.__name__)

        return self.result

    def subscribe(self, on_success: Callable, on_error: Callable, blocks=False):
        if on_success is None or on_error is None:
            raise ValueError("Illegal argument. Callbacks on_success and on_error must not be null")

        self.on_success = on_success
        self.on_error = on_error
        self.execute_on_caller = blocks

        if blocks:
            while not self.thread.is_alive():
                pass
            self.thread.join()
            if self.exception is None:
                on_success(self.result)
            else:
                on_error(self.exception)


class GlobalTaskManager:
    '''
    Singleton class designed to manage async tasks in a thread pool.
    Multiple instances of this class can cause unintended behaviour
    '''

    def __init__(self, max_thread=DEFAULT_MAX_THREADS):
        self.max_threads = max_thread
        self.thread_pool = []
        self.task_queue = Queue()

    def put(self, thread: Thread):
        self.task_queue.put(thread)

    def remove(self, thread: Thread):
        for t in self.thread_pool:
            if thread.ident == t.ident:
                self.thread_pool.remove(t)

    def run(self):
        while True:
            if len(self.thread_pool) < self.max_threads:
                child_thread: Thread = self.task_queue.get()
                child_thread.start()
                self.thread_pool.append(child_thread)


global_task_manager = GlobalTaskManager()
worker = Thread(target=global_task_manager.run, daemon=True)
worker.start()
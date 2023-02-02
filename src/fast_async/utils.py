from typing import List
from .types.tasks import AsyncTask
from .exceptions.task_exceptions import AsyncTaskException


def await_all(tasks: List[AsyncTask]):
    result = []
    for task in tasks:
        if task.status == 'pending':
            while not task.thread.is_alive():
                pass
            task.thread.join()

    for task in tasks:
        if task.status == 'success':
            result.append(task.result)
        elif task.status == 'failure':
            raise AsyncTaskException(str(task.exception), task.func.__name__)

    return result


def await_first(tasks: List[AsyncTask]):
    first_failed: AsyncTask = None
    while len(tasks) > 0:
        for i in range(len(tasks)):
            if tasks[i].status == 'success':
                return tasks[i].result
            elif tasks[i].status == 'failure':
                if first_failed is None:
                    first_failed = tasks[i]
                tasks.pop(i)
                i -= 1

    raise AsyncTaskException(str(first_failed.exception), first_failed.func.__name__)

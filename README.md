# Fast Async

![Publish to PyPi](https://github.com/thebowenfeng/FastAsync/actions/workflows/build_and_dist.yml/badge.svg)

A thread based, asynchronous programming framework built for Python.
Designed and optimized for speed. 

Asyncio, the go-to asynchronous programming framework for Python, uses
a single-threaded event loop to achieve concurrency. Although this prevents
unnecessary computational overheads and race conditions, it is inherently not
as fast as threads (even with inefficiencies brought along with GIL). In some
scenarios where speed is of utmost importance and where computational resources
are abundant, then it makes sense to use a multi-threading approach to concurrency.

Fast Async is a high-level API for Python `threads`, providing users with the
ability to `await` asynchronous code, and other features such as event-driven,
pubsub model (similar to Javascript's ```Promise.then()```). It aims to serve as
an alternative to asyncio, for users who require faster execution speed.

## Installation

Run ```pip install fast-async```

#### Running locally

Clone the repository and make the working directory ```src/```. 

Alternatively, extract the folder ```src/fast_async```.


## Benchmarks

#### Scenario (```sample.py```)

A long-running network request and an expensive operation is executed asynchronously

#### Result

```fast-async``` is, on average, almost 50% faster than ```asyncio``` due to
asyncio executing the two tasks almost sequentially whilst fast-async leverages threads
to execute them in parallel.

## FAQ

#### When to use fast-async

Fast-async should be used when execution speed is a higher priority.
For example, uploading each frame of a video stream to a remote server.
For cases where execution speed is not important, or when well-written code
make the speed differences negligible, asyncio is preferred.

#### What about ThreadPoolExecutor?

```ThreadPoolExecutor``` is a Python built-in class that offers some of the
same functionalities as fast-async, namely the ability to wait for tasks, and
limiting threads to conserve resources. However, fast-async is more feature-rich, 
such as the event-driven model (subscribers and callbacks) and various utility functions
that mirror certain useful functionalities from other languages (such as JavaScript). 
Fast-async is designed to enhance developer experience when working with threads, by
offering an easy-to-use interface and minimal pre-requisite knowledge.

## Documentation

### Decorators

```@make_async```

Make a function asynchronous. Functions that are decorated with 
```make_async``` will return an object of type ```AsyncTask```

Aside from its type, decorated functions can be treated as a normal function.
This means arguments can be passed in, much like a regular function.

Exceptions raised within the decorated function will be caught and re-thrown
in the caller thread.

#### Example:

```python
from fast_async import make_async

@make_async
def hello(message):
    print("hello world")
    return message

# Awaits hello to finish executing
return_val = hello("hello world").wait()

# Prints "hello world"
print(return_val)
```

### Classes

Package: fast_async.types.tasks

```class AsyncTask(func: Callable, *args, **kwargs)```

#### Attributes

- func: A function or ```Callable```.
- *args: Non-keyworded arguments for func
- **kwargs: Keyworded arguments for func
- status: Current status of func (pending, success, failure)
- result: Return value of func
- thread: ```Thread``` that func is being ran on
- exception: First caught ```Exception``` raised in func

#### Methods

```run()```

Runs ```func``` on a child thread, returns ```None```.

```wait()```

Awaits ```func``` to finish executing (blocks the caller thread),
returns the return value of ```func```.

```subscribe(on_success: Callable, on_failure: Callable, blocks: bool = False)```

Subscribes success and failure callbacks that is invoked when task is 
finished executing or raised an exception. Optional blocks argument 
controls whether subscribe blocks the caller thread (by default subscribe does not block)

### Functions

```set_max_threads(num: int): None```

Set the max number of threads available to be consumed by tasks.
Default is 64 threads. Useful when wanting to dynamically scale 
usage.

#### Example:

```python
from fast_async import set_max_threads

set_max_threads(3) # Only allows a maximum of 3 concurrent threads
```

```await_all(tasks: List[AsyncTask]): List```

Waits for all tasks in the ```tasks``` list to finish executing, or
when a task fails, then the function will immediately raise an exception and exit.

Returns a list of results corresponding to the list of tasks provided.

Similar to JavaScript's ```Promise.all()```

#### Example:

```python
from fast_async import make_async
from fast_async.utils import await_all

@make_async
def func1():
    return 1

@make_async
def func2():
    return 2

await_all([func1(), func2()]) # Will return [1, 2]
```

```await_first(tasks: List[AsyncTask]): Any```

Waits for the first task in ```tasks``` list to finish executing
and immediately returns the result. If all tasks fail, then the first
failed task is raised in an exception.

Returns the result of the first successful task.

Similar to JavaScript's ```Promise.race()```

#### Example

```python
from fast_async import make_async
from fast_async.utils import await_first
import time

@make_async
def func1():
    time.sleep(1)
    return 1

@make_async
def func2():
    time.sleep(2)
    return 2

await_first([func1(), func2()]) # Will return 1, because func1 finishes first
```

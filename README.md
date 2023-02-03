# Fast Async

![Publish to PyPi](https://github.com/thebowenfeng/FastAsync/actions/workflows/build_and_dist.yml/badge.svg)

A thread based, asynchronous programming framework built for Python, serving as
an easier-to-use and sometimes faster alternative to asyncio and co-routines.

Asyncio, the go-to asynchronous programming framework for Python, uses
a single-threaded event loop to achieve concurrency. Event loops (and co-routines in general),
relies on programs willingly yielding control to each other in order to achieve concurrency, also
known as "cooperative multitasking". Although this design pattern 
is fast and resource efficient, it requires users to be able to write well-designed code that can efficiently
yield control.

Unfortunately, this is often not the case. Python libraries are rarely designed to be
asynchronous. In order words, most Python code is "non-divisive", they will not
yield control to other functions, and therefore cannot take advantage of the event loops 
implemented  by asyncio. This means asyncio will most often than not execute (poorly designed)
"async" functions synchronously.

Fast Async solves this problem by utilizing threads to achieve concurrency.
Threads will always execute code in parallel*, with some resource overheads. This means that your code
can leverage Fast Async out of the box, without special configurations or refactoring, yet still
achieve concurrency.

Fast Async is a high-level API for Python `threads`, providing users with the
ability to `await` asynchronous code, and other features such as event-driven,
pubsub model (similar to Javascript's ```Promise.then()```). It aims to serve as
an alternative to asyncio, for users who require faster execution speed.

**Python threads does not achieve OS level TPL (thread level parallelism) due to GIL 
(global interpreter lock) making it that only 1 thread is ran at any time. That being said, for
the most part, they still mimic behaviours of native threads*

## Installation

Run ```pip install fast-async```

#### Running locally

Clone the repository and make the working directory ```src/```. 

Alternatively, extract the folder ```src/fast_async```.


## Benchmarks

#### Scenario (```src/sample.py```)

This scenario shows how detrimental poorly designed code are to asyncio's
performance.

Two functions, a network request and an expensive calculation is ran. Both
functions are non-divisive (i.e does not yield control to each other), and hence
asyncio will run both in sequential order.

#### Result

asyncio + aiohttp: 8.7s

fast-async + requests: 5.1s

```fast-async``` is, on average, almost 2x faster than ```asyncio``` due to
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


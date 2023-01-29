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

```def run()```

Runs ```func``` on a child thread, returns ```None```.

```def wait()```

Awaits ```func``` to finish executing (blocks the caller thread),
returns the return value of ```func```.


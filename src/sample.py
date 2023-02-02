from fast_async import make_async
from fast_async.utils import await_all, await_first
import time
import threading
import asyncio
import requests
import aiohttp


async def asyncio_network_req():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://hub.dummyapis.com/delay?seconds=3') as response:
            pass


async def expensive_function():
    j = 0
    for i in range(100000000):
        j *= 2
        j -= j


curr = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(asyncio_network_req(), expensive_function()))
print("Overall execution time with asycnio: ", time.time() - curr)

curr = time.time()


@make_async
def async_network_req():
    requests.get("https://hub.dummyapis.com/delay?seconds=3")


@make_async
def async_expensive_calc():
    j = 0
    for i in range(100000000):
        j *= 2
        j -= j


await_all([async_network_req(), async_expensive_calc()])
print("Overall execution time with fast-async: ", time.time() - curr)

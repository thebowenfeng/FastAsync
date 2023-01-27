from fast_async import make_async
import time


@make_async
def test_func2():
    print('inner test func')
    time.sleep(1)


@make_async
def test_func():
    test_func2().wait()
    print("outer test func")
    time.sleep(1)


test_func().wait()
print('main')
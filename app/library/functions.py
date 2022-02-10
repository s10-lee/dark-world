import asyncio
import time
import random
from datetime import datetime
from functools import wraps
from app.db.utils import close_connections


def get_timestamp(f="%H%M%S_%f"):
    return datetime.now().strftime(f)


def track_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        print('--- ', time.strftime('%H:%M:%S'), ' ---')
        result = f(*args, **kwargs)
        print(f'---  {round(time.time() - start, 2)} sec  ---')
        print('--- ', time.strftime('%H:%M:%S'), ' ---')
        return result
    return wrapper


def coro(function=None, keep_alive=False):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(f(*args, **kwargs))
            finally:
                if not keep_alive:
                    loop.run_until_complete(close_connections())
                loop.run_until_complete(asyncio.sleep(0.5))
        return wrapper
    if callable(function):
        return decorate(function)
    return decorate


def generate_unique_string(k=5):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = random.choices(chars, k=k)
    return ''.join(result)

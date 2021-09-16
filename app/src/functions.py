import asyncio
import json
import os
import time
from datetime import datetime
from functools import wraps
from tortoise import Tortoise


def track_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        print("--- ", time.strftime("%H:%M:%S"), " ---")
        result = f(*args, **kwargs)
        print(f"---  {round(time.time() - start, 2)} sec  ---")
        print("--- ", time.strftime("%H:%M:%S"), " ---")
        return result
    return wrapper


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(f(*args, **kwargs))
        finally:
            if f.__name__ != "cli":
                loop.run_until_complete(Tortoise.close_connections())
                loop.run_until_complete(asyncio.sleep(0.25))
    return wrapper


def chdir(path):
    p = os.path.dirname(path)
    os.chdir(p)
    return p


def get_timestamp(f="%H%M%S_%f"):
    return datetime.now().strftime(f)


def read_from_file(*args, filename, ext="json"):
    path = "/".join([*args]) + "/" + filename + "." + ext
    with open(path, "r") as fp:
        data = json.load(fp)
    return data


def save_to_file(content, *args, filename=None, mode="w", ext="json"):
    path = "/".join([*args])
    os.makedirs(path, exist_ok=True)

    if not filename:
        filename = get_timestamp()

    filepath = path + "/" + filename + "." + ext
    with open(filepath, mode) as fp:
        fp.write(content)
    return filepath


def import_driver(name, module="drivers"):
    parent = __import__(module, fromlist=[name])
    driver_module = getattr(parent, name)
    return driver_module.constructor

import json
import os
from datetime import datetime


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

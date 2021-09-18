from . import models
import random


def generate_unique_string(k=5):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = random.choices(chars, k=k)
    return ''.join(result)


async def create(url: str):
    code = generate_unique_string()
    item = await models.Link.create(url=url, code=code)
    return item


async def receive(code: str):
    return await models.Link.get_or_none(code=code)


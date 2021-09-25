import aiofile
import os


async def save_file(content, filepath, mode='w'):
    dirname = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(dirname, exist_ok=True)
    async with aiofile.async_open(filepath, mode) as fp:
        await fp.write(content)


async def read_file(filepath, mode='r'):
    async with aiofile.async_open(filepath, mode) as fp:
        return await fp.read()

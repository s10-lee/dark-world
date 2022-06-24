from app.settings import MEDIA_ROOT
from uuid import UUID
from typing import Type
from pathlib import PurePath
import aiofile
import os


def get_extension(file_path):
    last_part = str(file_path).split('.')[-1]
    return last_part.split('?')[0]


async def read_file(filepath, mode='r'):
    async with aiofile.async_open(filepath, mode) as fp:
        return await fp.read()


async def save_file(content, filepath, mode='w'):
    dirname = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(dirname, exist_ok=True)
    async with aiofile.async_open(filepath, mode) as fp:
        await fp.write(content)


async def save_file_media(
        content,
        path: [Type[PurePath], UUID, str],
        filename: [UUID, str],
        extension: str = None,
        mode: str = 'wb'
):
    return await save_file(
        content,
        MEDIA_ROOT / str(path) / (str(filename) + ('.' + str(extension) if extension else '')),
        mode=mode,
    )


async def remove_file_media(
        path: [Type[PurePath], UUID, str],
        filename: [UUID, str],
        extension: str = None,
):
    media_file_path = MEDIA_ROOT / str(path) / (str(filename) + ('.' + str(extension) if extension else ''))
    if os.path.exists(media_file_path):
        return os.unlink(media_file_path)
    return False

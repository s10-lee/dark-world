from fastapi import APIRouter, Depends, UploadFile, File, exceptions
from app.src.gallery.models import Pin
from app.library.files import save_file_media, remove_file_media
from uuid import uuid4, UUID
import os


async def create_pin(content: bytes, user_id: UUID, filename: str, content_type: str = None):
    primary_key = uuid4()
    extension = filename.rsplit('.')[-1]
    name = os.path.basename(filename)

    await save_file_media(content, path=user_id, filename=primary_key, extension=extension)
    pin = await Pin.create(
        id=primary_key,
        user_id=user_id,
        name=name,
        extension=extension,
        content_type=content_type,
    )
    return pin


async def upload_pin(file: UploadFile, user_id: UUID):
    return await create_pin(
        content=await file.read(),
        user_id=user_id,
        filename=file.filename,
        content_type=file.content_type,
    )

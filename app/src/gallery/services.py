from fastapi import APIRouter, Depends, UploadFile, exceptions
from app.src.gallery.models import Pin
from app.src.auth.services import get_current_user_id
from app.src.gallery.models import Pin
from app.library.files import save_file_media, remove_file_media
from uuid import uuid4, UUID


async def create_pin(file: UploadFile, user_id: UUID):
    primary_key = uuid4()

    extension = file.filename.split('.')[-1]
    content_type = file.content_type
    contents = await file.read()

    await save_file_media(contents, path=user_id, filename=primary_key, extension=extension)

    pin = await Pin.create(
        id=primary_key,
        user_id=user_id,
        name=file.filename,
        extension=extension,
        content_type=file.content_type,
    )

    return pin

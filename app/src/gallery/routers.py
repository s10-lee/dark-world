from fastapi import APIRouter, Depends, UploadFile
from app.src.auth.services import get_current_user_id
from app.src.gallery.models import Pin
from app.library.files import save_file_media
from uuid import uuid4, UUID
from app.src.gallery import schemas


router = APIRouter(tags=['Gallery'])


@router.get('/')
async def gallery_index(user_id: UUID = Depends(get_current_user_id)) -> schemas.PinList:
    return await schemas.PinList.from_queryset(Pin.filter(user_id=user_id))


@router.post('/upload/')
async def upload_media(file: UploadFile, user_id: UUID = Depends(get_current_user_id)) -> schemas.PinReceive:
    uid = uuid4()
    extension = file.filename.split('.')[-1]
    contents = await file.read()

    await save_file_media(contents, path=user_id, filename=uid, extension=extension)
    return await Pin.create(user_id=user_id, name=file.filename, uid=uid, extension=extension)

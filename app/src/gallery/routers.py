from fastapi import APIRouter, Depends, UploadFile, exceptions
from app.src.auth.services import get_current_user_id
from app.src.gallery.models import Pin
from app.library.files import save_file_media, remove_file_media
from uuid import uuid4, UUID
from app.src.gallery import schemas

router = APIRouter(tags=['Gallery'])


@router.get('/gallery/',)
async def gallery_index(user_id: UUID = Depends(get_current_user_id)) -> schemas.PinList:
    return await schemas.PinList.from_queryset(Pin.filter(user_id=user_id))


@router.post('/upload/')
async def upload_media(files: list[UploadFile], user_id: UUID = Depends(get_current_user_id)) -> schemas.PinList:
    pins = []
    for file in files:
        item_id = uuid4()
        extension = file.filename.split('.')[-1]
        contents = await file.read()
        await save_file_media(contents, path=user_id, filename=item_id, extension=extension)
        pin = await Pin.create(
            id=item_id,
            user_id=user_id,
            name=file.filename,
            extension=extension,
            content_type=file.content_type,
        )
        pins.append(
            await schemas.PinReceive.from_tortoise_orm(pin)
        )
    return pins


@router.delete('/gallery/{pk}/')
async def delete_media(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    pin = await Pin.get_or_none(pk=pk, user_id=user_id)
    try:
        await remove_file_media(user_id, pin.id, pin.extension)
        await pin.delete()
        return {'detail': 'deleted'}
    except Exception as e:
        return exceptions.HTTPException(400, detail=str(e))

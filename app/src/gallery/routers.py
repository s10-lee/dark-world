from fastapi import APIRouter, Depends, UploadFile, exceptions
from app.src.auth.services import get_current_user_id
from app.src.gallery.models import Pin
from app.library.files import remove_file_media
from uuid import UUID
from app.src.gallery import schemas
from app.src.gallery.services import upload_pin

router = APIRouter(tags=['Gallery'])


@router.get('/gallery/',)
async def gallery_index(user_id: UUID = Depends(get_current_user_id)) -> schemas.PinList:
    return await schemas.PinList.from_queryset(Pin.filter(user_id=user_id))


@router.post('/upload/')
async def upload_media(files: list[UploadFile], user_id: UUID = Depends(get_current_user_id)) -> schemas.PinList:
    pins = []
    for file in files:
        pin = await upload_pin(file=file, user_id=user_id)
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

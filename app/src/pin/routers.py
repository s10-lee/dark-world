from fastapi import APIRouter, Request, Depends, UploadFile
from app.library.web import make_request
# from app.src.user.models import User
from app.src.auth.services import get_current_user_id
from app.src.grab.services import grab_from_pinterest
from app.src.pin.models import Pin
from app.library.files import save_file
from app.settings import MEDIA_ROOT
from uuid import uuid4, UUID
from app.src.pin.schemas import PinSchemaList, PinSchemaReceive, PinSchemaGrab


router = APIRouter(tags=['Pin'])


@router.get('/')
async def list_pins(user_id: UUID = Depends(get_current_user_id)) -> PinSchemaList:
    return await PinSchemaList.from_queryset(Pin.filter(user_id=user_id))


@router.post('/upload/')
async def upload_pin(file: UploadFile, user_id: UUID = Depends(get_current_user_id)) -> PinSchemaReceive:
    uid = uuid4()
    extension = file.filename.split('.')[-1]
    contents = await file.read()

    await save_file(contents, f'{MEDIA_ROOT}/{user_id}/{uid}.{extension}', mode='wb')
    return await Pin.create(user_id=user_id, name=file.filename, uid=uid, extension=extension)


@router.post('/grab/')
async def grab_pin(data: PinSchemaGrab, user_id: UUID = Depends(get_current_user_id)):
    uid = uuid4()
    url = data.url

    # TODO: Grab service
    if url.host == 'www.pinterest.com':
        url = await grab_from_pinterest(url)

    extension = url.split('.')[-1]
    response = await make_request(url, data_format='binary')

    if response.status == 200:
        await save_file(response.data, f'{MEDIA_ROOT}/{user_id}/{uid}.{extension}', mode='wb')
        return await Pin.create(user_id=user_id, name='', uid=uid, extension=extension)

    return {'status': response.status}


# @router.get('/{pk}/')
# async def receive_pin(pk, user_id: UUID = Depends(get_current_user_id)) -> PinSchemaReceive:
#     return await PinSchemaReceive.from_tortoise_orm(Pin.get(id=pk))
#
#
# @router.patch('/{pk}/')
# async def update_pin(pk):
#     return {'data': True}


# @router.get('/private-route/')
# async def private_route(user: User = Depends(auth_wrapper)):
#     return {'user': user}

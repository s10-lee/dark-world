from fastapi import APIRouter, Request, Depends, UploadFile
from app.src.user.models import User
from app.src.auth.services import auth_wrapper
from typing import Optional
from app.src.pin.models import Pin
from app.library.files import save_file
from app.settings import MEDIA
from uuid import uuid4
# from app.src.pin.schemas import SchemaReceive, SchemaCreate, SchemaList


router = APIRouter()


@router.get('/')
async def get_user_files(user_data: dict = Depends(auth_wrapper)):
    items = await Pin.filter(user_id=user_data['sub'])
    return items


@router.post('/upload/')
async def upload_file(file: UploadFile, user_data: dict = Depends(auth_wrapper)):
    user_id = user_data['sub']
    file_name = uuid4()
    file_ext = file.filename.rsplit('.')[-1]

    contents = await file.read()
    await save_file(contents, f'app/media/{user_id}/{file_name}.{file_ext}', mode='wb')
    await Pin.create(user_id=user_id, name=file.filename, uid=file_name)

    return {'filename': file.filename, 'extension': file_ext}


@router.get('/test/')
async def private_route(user_data: dict = Depends(auth_wrapper)):
    return {'user': user_data['sub']}


# @router.get('/public-route/')
# async def public_route(request: Request):
#     return {'user': request.state.user}
#
#
# @router.get('/private-route/')
# async def private_route(user: User = Depends(auth_wrapper)):
#     return {'user': user}

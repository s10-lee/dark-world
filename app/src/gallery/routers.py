from fastapi import APIRouter, Depends, UploadFile
from app.library.web import make_request
from app.src.auth.services import get_current_user_id
from app.src.gallery.services import grab_from_pinterest
from app.src.gallery.models import MediaItem
from app.library.files import save_file
from app.settings import MEDIA_ROOT
from uuid import uuid4, UUID
from app.src.gallery import schemas


router = APIRouter(tags=['Gallery'])


@router.get('/')
async def gallery_index(user_id: UUID = Depends(get_current_user_id)) -> schemas.MediaItemList:
    return await schemas.MediaItemList.from_queryset(MediaItem.filter(user_id=user_id))


@router.post('/upload/')
async def upload_media(file: UploadFile, user_id: UUID = Depends(get_current_user_id)) -> schemas.MediaItemReceive:
    uid = uuid4()
    extension = file.filename.split('.')[-1]
    contents = await file.read()

    await save_file(contents, f'{MEDIA_ROOT}/{user_id}/{uid}.{extension}', mode='wb')
    return await MediaItem.create(user_id=user_id, name=file.filename, uid=uid, extension=extension)


@router.post('/grab/')
async def grab_media(data: schemas.MediaItemGrab, user_id: UUID = Depends(get_current_user_id)):
    uid = uuid4()
    url = data.url

    # TODO: Grab service
    if url.host == 'www.pinterest.com':
        url = await grab_from_pinterest(url)

    extension = url.split('.')[-1]
    response = await make_request(url, data_format='binary')

    if response.status == 200:
        await save_file(response.data, f'{MEDIA_ROOT}/{user_id}/{uid}.{extension}', mode='wb')
        return await MediaItem.create(user_id=user_id, name='', uid=uid, extension=extension)

    return {'status': response.status}


from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import get_request_binary
from app.src.user.services import save_file_media
from app.src.gallery.models import Pin
from app.src.grab.services import grab_from_pinterest
from app.src.grab.schemas import GrabUrl
import uuid


router = APIRouter(tags=['Grabbers'])


@router.post('/grab/')
async def grab_media_from_url(data: GrabUrl, user_id: uuid.UUID = Depends(get_current_user_id)):
    unique_uid = uuid.uuid4()
    url = data.url

    # TODO: Grab service
    if url.host == 'www.pinterest.com':
        url = await grab_from_pinterest(url)

    ext = url.split('.')[-1]
    response = await get_request_binary(url)

    if response.status == 200:
        await save_file_media(response.data, user_id, unique_uid, extension=ext)
        return await Pin.create(user_id=user_id, uid=unique_uid, extension=ext)

    return {'status': response.status}





from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import get_request_binary
from app.library.files import save_file_media
from app.src.gallery.models import Pin
from app.src.gallery.schemas import PinReceive
from app.src.grab.services import grab_from_pinterest, grab_from_dribble
from app.src.grab.schemas import GrabUrl
import uuid


router = APIRouter(tags=['Grabbers'])


@router.post('/grab/')
async def grab_media_from_url(data: GrabUrl, user_id: uuid.UUID = Depends(get_current_user_id)):
    item_id = uuid.uuid4()
    url = data.url

    # TODO: Grab service
    if url.host == 'www.pinterest.com':
        url = await grab_from_pinterest(url)

    if url.host == 'dribbble.com':
        url = await grab_from_dribble(url)

    extension = url.split('.')[-1]
    response = await get_request_binary(url)

    if response.status == 200 and url:
        await save_file_media(response.data, path=user_id, filename=item_id, extension=extension)
        return await PinReceive.from_tortoise_orm(
            await Pin.create(id=item_id, user_id=user_id, name=url.host, extension=extension)
        )

    return {'status': response.status}





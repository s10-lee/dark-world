from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import parse_html_response, send_http_request, MyResponse
# from app.src.gallery.schemas import PinReceive
from app.src.gallery.services import create_pin
from app.src.grab.schemas import GrabberSchema
import uuid
from pprint import pp
from typing import Union


router = APIRouter(tags=['Grabbers'])


@router.post('/grab/')
async def grab_media_from_url(data: GrabberSchema, user_id: uuid.UUID = Depends(get_current_user_id)):
    url = data.url
    hostname = url.host
    pattern = ''
    elements = [url]
    result = dict()

    response = await send_http_request(url, debug=True)
    if hostname == 'www.pinterest.com':
        pattern = '//head/link[@as="image"]/@href'

    if hostname == 'dribbble.com':
        # //head/meta[@property="og:image"]/@content
        pattern = '//img[@data-animated-url]/@data-animated-url'

    if pattern:
        elements = await parse_html_response(response.body, pattern=pattern)

    for el in elements:
        print(el)
        response = await send_http_request(url)
        result[el] = response.status

        # if 400 > response.status >= 200 and elements:
        #     if data.save:
        #         await create_pin(content=response.body, user_id=user_id, filename=url, content_type=response.content_type)

    return result


@router.post('/grab/html/')
async def grab_html_from_url(
        data: GrabberSchema,
        user_id: uuid.UUID = Depends(get_current_user_id)
) -> dict[str, Union[MyResponse, list]]:

    url = data.url
    elements = []

    response = await send_http_request(url, debug=True)
    if data.pattern:
        elements = await parse_html_response(response.body, pattern=data.pattern)

    result = {
        'elements': elements,
        'response': response,
    }

    return result

# async def download_media_file


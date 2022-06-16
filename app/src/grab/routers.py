from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import parse_html_response, send_http_request
from app.src.gallery.services import create_pin
from app.src.grab import schemas
# from app.src.grab.models import Grabber
from app.src.grab.models import HttpHeader, HttpMethod, Collection
from urllib.parse import urlparse
from io import BytesIO
from pytube import YouTube
import uuid
import ssl

# TODO: Fix this shit
ssl._create_default_https_context = ssl._create_unverified_context


router = APIRouter(tags=['Grabbers'])


@router.get('/http-headers/')
async def list_headers():
    return await HttpHeader.all()


@router.get('/http-methods/')
async def list_methods():
    return {item.name: item.value for item in HttpMethod}


@router.options('/http-collection/')
async def config_collections(user_id: uuid.UUID = Depends(get_current_user_id)):
    return {

    }


@router.get('/http-collection/')
async def list_collections(user_id: uuid.UUID = Depends(get_current_user_id)):
    return await schemas.CollectionList.from_queryset(Collection.filter(user_id=user_id))


@router.get('/http-collection/{pk}/', response_model=schemas.CollectionReceive)
async def receive_collection(pk: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id)):
    return await Collection.get(id=pk, user_id=user_id)


@router.put('/http-collection/{pk}/', response_model=schemas.CollectionReceive)
async def update_collection(pk: uuid.UUID, data: schemas.CollectionCreate, user_id: uuid.UUID = Depends(get_current_user_id)):
    item = await Collection.get(id=pk, user_id=user_id)
    await item.update_from_dict(data.dict(exclude_unset=True)).save()
    return item


@router.post('/http-collection/', response_model=schemas.CollectionReceive)
async def create_collection(data: schemas.CollectionCreate, user_id: uuid.UUID = Depends(get_current_user_id)):
    item = await Collection.create(**data.dict(), user_id=user_id)
    return item


@router.delete('/http-collection/{pk}/')
async def destroy_collection(pk: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id)):
    await Collection.filter(id=pk, user_id=user_id).delete()
    return {}


# @router.post('/grab/html/')
# async def grab_html_from_url(data: GrabberSchema, user_id: uuid.UUID = Depends(get_current_user_id)):
#     url = data.url
#     elements = {}
#     response = await send_http_request(url)
#
#     if data.pattern:
#         res = parse_html_response(response.body, pattern=data.pattern)
#
#         for el in res:
#             resp = await send_http_request(el, raw=True)
#             elements[el] = resp.status
#
#             if 300 > resp.status >= 200 and el and data.save:
#                 await create_pin(content=resp.body, user_id=user_id, filename=el, content_type=resp.content_type)
#
#     return {
#         'elements': elements,
#         'response': response,
#     }


# @router.post('/grab/download/')
# async def download_media_file(url, user_id: uuid.UUID = Depends(get_current_user_id)):
#     resp = await send_http_request(url, raw=True, debug=True)
#     item = dict()
#     if 300 > resp.status >= 200 and resp.content_type:
#         item = await create_pin(content=resp.body, user_id=user_id, filename=url, content_type=resp.content_type)
#     return item


# @router.post('/grab/youtube/')
# async def grab_video_from_youtube(data: GrabberYoutubeSchema, user_id: uuid.UUID = Depends(get_current_user_id)):
#     yt = YouTube(data.url)
#     result = []
#
#     streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
#     for stream in streams:
#         result.append({'value': stream.itag, 'text': f'{stream.resolution} ({stream.fps}fps)'})
#
#     if data.itag:
#         buffer = BytesIO()
#         stream = yt.streams.get_by_itag(data.itag)
#         stream.stream_to_buffer(buffer)
#         buffer.seek(0)
#         content = buffer.read()
#         await create_pin(content, user_id, filename=stream.title + '.mp4', content_type=stream.mime_type)
#
#     return {
#         'title': yt.title,
#         'thumbnail': yt.thumbnail_url,
#         'streams': result,
#     }

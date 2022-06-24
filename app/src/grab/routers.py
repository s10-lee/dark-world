from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import parse_html_response, send_http_request, HttpRequest
from app.src.gallery.services import create_pin
from app.src.grab import schemas
# from app.src.grab.models import Grabber
from app.src.grab.models import HttpHeader, HttpMethod, Collection, Request, Variable, Grabber
from urllib.parse import urlparse, urljoin
from app.src.grab.services import GRAB_UTILS, filter_json
from io import BytesIO
from pytube import YouTube
from uuid import UUID
import orjson
import ssl

# TODO: Fix this shit
ssl._create_default_https_context = ssl._create_unverified_context


router = APIRouter(tags=['HTTP'])


@router.get('/grab/')
async def get_grabbers():
    return await Grabber.all()


# @router.get('/http-headers/')
# async def list_headers(user_id: UUID = Depends(get_current_user_id)):
#     return await HttpHeader.all()


@router.get('/http-methods/')
async def list_methods(user_id: UUID = Depends(get_current_user_id)):
    return {item.name: item.value for item in HttpMethod}


# ---------------- #
#    Collection    #
# ---------------- #

@router.get('/http-collection/')
async def list_collections(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.CollectionList.from_queryset(Collection.filter(user_id=user_id))


@router.post('/http-collection/')
async def create_collection(data: schemas.CollectionCreate, user_id: UUID = Depends(get_current_user_id)):
    item = await Collection.create(**data.dict(exclude_unset=True), user_id=user_id)
    return await schemas.CollectionReceive.from_tortoise_orm(item)


@router.get('/http-collection/{pk}/', response_model=schemas.CollectionReceive)
async def receive_collection(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await Collection.get(id=pk, user_id=user_id).prefetch_related('requests', 'variables')


@router.put('/http-collection/{pk}/', response_model=schemas.CollectionReceive)
async def update_collection(pk: UUID, data: schemas.CollectionCreate, user_id: UUID = Depends(get_current_user_id)):
    item = await Collection.get(id=pk, user_id=user_id)
    await item.update_from_dict(data.dict(exclude_unset=True)).save()
    return item


@router.delete('/http-collection/{pk}/')
async def destroy_collection(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await Collection.filter(id=pk, user_id=user_id).delete()


# ------------- #
#    Request    #
# ------------- #

@router.get('/http-request/')
async def list_requests(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.RequestList.from_queryset(Request.filter(collection__user__id=user_id))


@router.get('/http-request/{pk}/', response_model=schemas.RequestReceive)
async def receive_request(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await Request.get(id=pk, collection__user__id=user_id)


@router.post('/http-request/', response_model=schemas.RequestReceive)
async def create_request(data: schemas.RequestCreate, user_id: UUID = Depends(get_current_user_id)):
    return await Request.create(**data.dict(exclude_unset=True))


@router.put('/http-request/{pk}/', response_model=schemas.RequestReceive)
async def update_request(pk: UUID, data: schemas.RequestCreate, user_id: UUID = Depends(get_current_user_id)):
    item = await Request.get(id=pk, collection__user__id=user_id)
    await item.update_from_dict(data.dict(exclude_unset=True)).save()
    return item


@router.get('/http-request/{pk}/exec/')
async def execute_request(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    req = await Request.get(id=pk, collection__user__id=user_id)
    await req.fetch_related('collection')

    request_data = {
        'method': req.method,
        'url': req.url,
        'params': filter_json(req.params),
        'headers': filter_json(req.headers),
        'data': req.data,
        'cookies': req.cookies,
    }

    prepared_request = orjson.dumps(request_data).decode('utf-8')

    for v in await req.collection.variables.all():
        replace_value = v.value
        if v.call:
            replace_value = GRAB_UTILS.get(v.call)()
        prepared_request = prepared_request.replace('{{' + v.name + '}}', replace_value)

    for name, callback in GRAB_UTILS.items():
        prepared_request = prepared_request.replace('{{@' + name + '}}', callback())

    prepared_request_data = orjson.loads(prepared_request.encode('utf-8'))

    return await send_http_request(**prepared_request_data, debug=True, convert='json')


# --------------- #
#    Variables    #
# --------------- #
# @router.get('/http-variable/')
# async def list_variables(user_id: UUID = Depends(get_current_user_id)):
#     return await schemas.VariableList.from_queryset(Variable.filter(collection__user__id=user_id))
#
#
# @router.post('/http-variable/', response_model=schemas.VariableReceive)
# async def create_variable(data: schemas.VariableCreate, user_id: UUID = Depends(get_current_user_id)):
#     return await Variable.create(**data.dict())
#
#
# @router.delete('/http-variable/{pk}/')
# async def destroy_variable(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
#     return await Variable.filter(id=pk, collection__user__id=user_id).delete()


# --------------- #
#     Execute     #
# --------------- #
@router.get('/http-execute/{pk}/')
async def pipeline_execute(pk: UUID):
    collection = await Collection.get(id=pk).prefetch_related('variables', 'requests')
    # item = await schemas.CollectionReceive.from_tortoise_orm(collection)
    # item = (await schemas.RequestReceive.from_tortoise_orm(r)).json()
    item = {}
    for r in collection.requests:

        params = filter_json(r.params)
        headers = filter_json(r.headers)

        request_data = {
            'method': r.method,
            'url': r.url,
            'params': params,
            'headers': headers,
            'data': r.data,
            'cookies': r.cookies,
        }

        prepared_request = orjson.dumps(request_data).decode('utf-8')

        for v in collection.variables:
            replace_value = v.value
            if v.call:
                replace_value = GRAB_UTILS.get(v.call)()
            prepared_request = prepared_request.replace('{{' + v.name + '}}', replace_value)

        for name, callback in GRAB_UTILS.items():
            prepared_request = prepared_request.replace('{{@' + name + '}}', callback())

        prepared_request_data = orjson.loads(prepared_request.encode('utf-8'))
        item = prepared_request_data

        resp = await send_http_request(**prepared_request_data, debug=True)
        item = resp

    return item


@router.post('/grab/html/')
async def grab_html_from_url(data: schemas.GrabberSchema, user_id: UUID = Depends(get_current_user_id)):
    url = data.url
    elements = {}
    response = await send_http_request('get', url)

    if data.pattern:
        res = parse_html_response(response.body, pattern=data.pattern)

        for el in res:
            resp = await send_http_request('get', el, raw=True)
            elements[el] = resp.status

            if 300 > resp.status >= 200 and el and data.save:
                await create_pin(content=resp.body, user_id=user_id, filename=el, content_type=resp.content_type)

    return {
        'elements': elements,
        'response': response,
    }


# @router.post('/grab/download/')
# async def download_media_file(url, user_id: UUID = Depends(get_current_user_id)):
#     resp = await send_http_request('get', url, raw=True, debug=True)
#     item = dict()
#     if 300 > resp.status >= 200 and resp.content_type:
#         item = await create_pin(content=resp.body, user_id=user_id, filename=url, content_type=resp.content_type)
#     return item


@router.post('/grab/youtube/')
async def grab_video_from_youtube(data: schemas.GrabberYoutubeSchema, user_id: UUID = Depends(get_current_user_id)):
    yt = YouTube(data.url)
    result = []

    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    for stream in streams:
        result.append({'value': stream.itag, 'text': f'{stream.resolution} ({stream.fps}fps)'})

    if data.itag:
        buffer = BytesIO()
        stream = yt.streams.get_by_itag(data.itag)
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        content = buffer.read()
        await create_pin(content, user_id, filename=stream.title + '.mp4', content_type=stream.mime_type)

    return {
        'title': yt.title,
        'thumbnail': yt.thumbnail_url,
        'streams': result,
    }

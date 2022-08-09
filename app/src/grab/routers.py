from fastapi import APIRouter, Depends
from app.src.auth.services import get_current_user_id
from app.library.web import parse_html_response, send_http_request
from app.src.gallery.services import create_pin
from app.src.grab import schemas
from app.src.grab.models import Grabber
from urllib.parse import urlparse, urljoin
from io import BytesIO
from pytube import YouTube
from uuid import UUID
import ssl

# TODO: Fix this shit
ssl._create_default_https_context = ssl._create_unverified_context


router = APIRouter(tags=['HTTP'])


@router.get('/grab/')
async def get_grabbers():
    return await Grabber.all()


@router.post('/grab/html/')
async def grab_html_from_url(data: schemas.GrabberSchema, user_id: UUID = Depends(get_current_user_id)):
    import urllib
    url = data.url
    response = await send_http_request('get', url)
    elements = []

    if data.pattern:
        if data.update_id:
            await Grabber.filter(id=data.update_id).update(search_xpath=data.pattern)

        parsed_url = urllib.parse.urlparse(url)
        netloc = parsed_url.netloc
        scheme = parsed_url.scheme

        if response.body:
            found = parse_html_response(response.body, pattern=data.pattern)

            for el in found:
                try:
                    result = urllib.parse.urlparse(el)

                    if not result.netloc:
                        parsed = urllib.parse.urlparse(result.geturl())
                        result = parsed._replace(netloc=netloc)

                    if not result.scheme:
                        parsed = urllib.parse.urlparse(result.geturl())
                        result = parsed._replace(scheme=scheme)

                    is_url = all([result.scheme, result.netloc])
                    result = result.geturl()

                    print(is_url, '=', result)
                except Exception as e:
                    print('ERROR:', e, '=', el)
                    result = el
                    is_url = False

                elements.append({'result': result, 'is_url': is_url})

                if data.save and is_url:
                    resp = await send_http_request('get', result, raw=True)
                    if 300 > resp.status >= 200 and resp.content_type.startswith('image'):
                        await create_pin(content=resp.body, user_id=user_id, filename=result, content_type=resp.content_type)
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

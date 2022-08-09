from app.library.web import parse_html_response, send_http_request
from app.src.gallery.services import create_pin


async def action_save_to_variable(name, variables, data):
    variables[name] = data
    return variables


async def action_save_img_to_file(url, user_id):
    resp = await send_http_request('GET', url, raw=True)
    item = dict()
    if 300 > resp.status >= 200 and resp.content_type:
        item = await create_pin(content=resp.body, user_id=user_id, filename=url, content_type=resp.content_type)
    return item


class RunnerService:
    pass

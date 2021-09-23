from fastapi import APIRouter, Request, Depends, HTTPException, Response, FastAPI
from fastapi.exceptions import StarletteHTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from app.src.auth.services import validate_signup
from app.config.settings import DEBUG, MODE
import json
import os


templates = Jinja2Templates(directory='app/templates')

web_router = APIRouter()


# @web_app.exception_handler(StarletteHTTPException)
# async def custom_exception_handler(request: Request, exc: StarletteHTTPException):
#     data = {
#         'request': request,
#         'exc': exc,
#         **get_vue()
#     }
#
#     print('exception', exc.detail)
#     print(exc.status_code)
#
#     if exc.status_code == 404:
#         return templates.TemplateResponse('layout_vue.html', data)
#
#     return await http_exception_handler(request, exc)

def get_vue() -> dict:
    stats_file = 'stats/webpack-stats.json'
    if MODE:
        stats_file = f'stats/webpack-stats-f{MODE}.json'

    stats_path = os.path.abspath(stats_file)
    styles = []
    scripts = []
    if os.path.exists(stats_path):
        with open(stats_path) as fp:
            data = json.load(fp)
            public_path = data['publicPath']
            for app_name in data['chunks']:
                for chunk in data['chunks'][app_name]:
                    file_name = chunk['name']
                    if file_name[-4:] == '.css':
                        styles.append(public_path + file_name)
                    if file_name[-3:] == '.js' and '.hot' not in file_name:
                        scripts.append(public_path + file_name)

    return {'styles': styles, 'scripts': scripts}


@web_router.get('/project', name='project test')
@web_router.get('/l1nk', name='show form')
@web_router.get('/', name='home')
async def show_client_layout(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse('layout_vue.html', {'request': request, **get_vue()})


@web_router.get('/sign-up/{uid}/')
async def signup_form(request: Request, uid: str = Depends(validate_signup)):
    return templates.TemplateResponse('sign_up.html', {'request': request, 'uid': uid})

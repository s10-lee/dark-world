from fastapi import APIRouter, Request, Depends, HTTPException, Response, FastAPI
from fastapi.exceptions import StarletteHTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from app.src.auth.services import validate_signup
from app.settings import MODE
import json
import os


templates = Jinja2Templates(directory='app/templates')
web_router = APIRouter()
web = FastAPI(default_response_class=HTMLResponse)


@web.exception_handler(StarletteHTTPException)
async def custom_exception_handler(request: Request, exc: StarletteHTTPException):
    # TODO: Make middleware
    # - for application/json return {"detail": "Not Found"}
    # - */* return HTML template response (404)

    data = {
        'request': request,
        'exc': exc,
        **get_vue()
    }

    if exc.status_code == 404 and not request.url.path.startswith('/api'):
        return templates.TemplateResponse('layout_vue.html', data)

    return await http_exception_handler(request, exc)


def get_vue() -> dict:
    # TODO: Make Jinja plugin / helper
    stats_file = 'stats/webpack-stats.json'
    if MODE:
        stats_file = f'stats/webpack-stats-{MODE}.json'

    stats_path = os.path.abspath(stats_file)
    styles = []
    scripts = []

    if not os.path.exists(stats_path):
        raise FileNotFoundError

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


@web_router.get('/', name='home', response_class=HTMLResponse)
async def show_client_layout(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse('layout_vue.html', {'request': request, **get_vue()})


@web_router.get('/sign-up/{uid}/', response_class=HTMLResponse)
async def signup_form(request: Request, uid: str = Depends(validate_signup)):
    return templates.TemplateResponse('sign_up.html', {'request': request, 'uid': uid, **get_vue()})



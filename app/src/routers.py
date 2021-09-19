from fastapi import APIRouter, Request, Depends, HTTPException, Response, FastAPI
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import StarletteHTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.src.user.routers import router as api_user
from app.src.link.routers import router as api_link
from app.src.auth.services import validate_signup
import json
import os

templates = Jinja2Templates(directory='app/templates')

api_router = APIRouter()
api_router.include_router(api_user)
api_router.include_router(api_link, prefix='/link')

web = FastAPI(default_response_class=HTMLResponse)


@web.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse('layout_vue.html', {'request': request, **get_vue()})
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)


def get_vue():
    stats_path = os.path.abspath('./stats/webpack-stats.json')
    styles = []
    scripts = []
    if os.path.exists(stats_path):
        with open(stats_path) as fp:
            data = json.load(fp)
            public_path = data['publicPath']
            for app_name in data['chunks']:
                print(app_name)
                for chunk in data['chunks'][app_name]:
                    file_name = chunk['name']

                    if file_name.endswith('.css'):
                        styles.append(public_path + file_name)

                    if file_name[-3:] == '.js':
                        scripts.append(public_path + file_name)
    return {'styles': styles, 'scripts': scripts}


# @web_router
# async def http_exception_handler(request, exc):
#     return Response(str(exc.detail), status_code=exc.status_code)


@web.get('/sign-up/{uid}/')
async def signup_form(request: Request, uid: str = Depends(validate_signup)):
    return templates.TemplateResponse('sign_up.html', {'request': request, 'uid': uid})


@web.get('/', name='Home')
@web.get('/n00b/')
async def show_user_profile(request: Request):
    return templates.TemplateResponse('layout_vue.html', {'request': request, **get_vue()})


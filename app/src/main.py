from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .security import (
    authentication_user,
    create_access_token,
    auth_wrapper,
    validate_signup,
    get_password_hash,
    create_refresh_token,
    auth_check_refresh
)
from tortoise.contrib.fastapi import register_tortoise
from .settings import ORM
from .models import User, UserCredentials, SignUpToken
from uuid import UUID
from datetime import datetime

app = FastAPI()
app.mount('/static', StaticFiles(directory='src/static'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
templates = Jinja2Templates(directory='src/templates')


async def client_token_response(user):
    refresh_token = await create_refresh_token(user)
    access_token = await create_access_token(user)
    response = JSONResponse(content={
        'access_token': access_token,
    })
    seconds = refresh_token.expires()
    response.set_cookie(
        key='refresh_token',
        value=refresh_token.token,
        expires=seconds,
        path='/',
        httponly=True,
    )
    return response


@app.get('/sign-up/{uid}/', name='signup form')
async def show_signup_form(request: Request, uid: UUID = Depends(validate_signup)):
    return templates.TemplateResponse('sign_up.html', {'request': request, 'uid': uid})


@app.post('/sign-up/{uid}/')
async def register_new_user(data: UserCredentials, uid: UUID = Depends(validate_signup)):
    if not (data.password and data.username):
        raise HTTPException(400, detail='All fields are required')

    try:
        await User.create(username=data.username, password=get_password_hash(data.password))
        await SignUpToken.filter(id=uid).update(activated_at=datetime.utcnow())
        return {'status': 'Success', 'detail': 'User created !'}
    except Exception as e:
        raise HTTPException(400, detail='User already exists')


# @app.get('/sign-in/')
# async def show_login_form(request: Request):
#     return templates.TemplateResponse('sign_in.html', {'request': request})


@app.post('/token/obtain/')
async def auth_obtain_token(user: User = Depends(authentication_user)):
    return await client_token_response(user)


@app.post('/token/refresh/')
async def auth_refresh_token(user: User = Depends(auth_check_refresh)):
    return await client_token_response(user)


@app.get('/profile/')
async def user_profile(user: User = Depends(auth_wrapper)):
    return {'access': 'yes', 'user': user}


register_tortoise(app, config=ORM)

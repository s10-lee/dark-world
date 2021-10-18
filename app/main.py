
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.auth.services import auth_wrapper
from app.src.user.routers import router as api_user
from app.src.link.routers import router as api_link
from app.src.grab.routers import router as api_grab
from app.src.web.routers import web_router, web
from app.config.settings import ORM, CORS_ALLOW_ORIGINS, APP_PARAMS

app = FastAPI(**APP_PARAMS)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(web_router)
app.include_router(api_user, prefix='/api/v1')
app.include_router(api_link, prefix='/api/v1/link')
app.include_router(api_grab, prefix='/api/v1/ws')
# dependencies=[Depends(auth_wrapper)]


app.mount('/', web)

register_tortoise(app, config=ORM)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.routers import api_router, web
from app.config.settings import ORM

app = FastAPI(prefix='/api/v1')

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api_router)
app.mount('/', web)

register_tortoise(app, config=ORM)

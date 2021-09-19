from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from app.src.routers import api_router, client_redirect
from app.src.web.routers import web_router
from app.config.settings import ORM, DEBUG


cors_origins = [
    'https://d4rkvv0r1.de',
    'http://localhost',
    'http://localhost:8000',
    'http://0.0.0.0',
    'http://0.0.0.0:8000'
]

app_kwargs = {'redoc_url': None}
if not DEBUG:
    app_kwargs['docs_url'] = None

app = FastAPI(**app_kwargs)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/1/{code}')
async def redirect(code: str):
    return await client_redirect(code)

app.include_router(web_router)
app.include_router(api_router, prefix='/api/v1')



register_tortoise(app, config=ORM)

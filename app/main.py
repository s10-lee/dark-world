from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.user.routers import router as api_user
from app.src.gallery.routers import router as api_gallery
from app.src.grab.routers import router as api_grab

from app.src.web.routers import web_router, web
from app.settings import ORM, CORS_ALLOW_ORIGINS, APP_PARAMS, DEBUG, MEDIA_URL, MEDIA_ROOT

app = FastAPI(**APP_PARAMS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(web_router)
app.include_router(api_user, prefix='/api')
app.include_router(api_gallery, prefix='/api')
app.include_router(api_grab, prefix='/api')

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name='media')
app.mount('/', web)


if not DEBUG:
    @app.get("/redoc", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def get_docs():
        return HTTPException(status_code=404)


register_tortoise(app, config=ORM)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.user.routers import router as api_user
from app.src.project.routers import router as project_router


from app.src.web.routers import web_router, web
from app.settings import ORM, CORS_ALLOW_ORIGINS, APP_PARAMS, DEBUG, MEDIA_URL, MEDIA_ROOT, STATIC_ROOT, STATIC_URL

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
app.include_router(project_router, prefix='/api')


app.mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT), name='static')
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name='media')
app.mount('/', web)


if not DEBUG:
    @app.get("/redoc", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def get_docs():
        return HTTPException(status_code=404)


register_tortoise(app, config=ORM)

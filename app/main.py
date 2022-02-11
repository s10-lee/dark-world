from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.user.routers import router as api_user
from app.src.web.routers import web_router, web
from app.src.auth.services import auth_wrapper, security
from app.settings import ORM, CORS_ALLOW_ORIGINS, APP_PARAMS, DEBUG, MEDIA_URL, MEDIA_ROOT

app = FastAPI(**APP_PARAMS)
app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name='media')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(web_router)
app.include_router(api_user, prefix='/api')

app.mount('/', web)


@app.middleware('http')
async def get_current_user_middleware(request: Request, call_next):
    request.state.user = None
    url_path = request.url.path

    if url_path.startswith('/api') and not url_path.startswith('/api/obtain'):
        try:
            auth = await security(request)
            user_data = await auth_wrapper(auth)
            request.state.user = {
                'id': user_data['sub'],
                'username': user_data['name'],
            }
        except Exception as e:
            print('Exception in middleware')
            print(repr(e))

    return await call_next(request)


if not DEBUG:
    @app.get("/redoc", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def get_docs():
        return HTTPException(status_code=404)


register_tortoise(app, config=ORM)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.user.routers import router as api_user
from app.src.grab.routers import router as api_grab
# from app.src.miro.routers import router as api_miro
from app.src.pin.routers import router as api_pin
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
app.include_router(api_grab, prefix='/api/ws')
# app.include_router(api_miro, prefix='/api/miro')
app.include_router(api_pin, prefix='/api/pin')

app.mount('/', web)


@app.middleware('http')
async def get_current_user_middleware(request: Request, call_next):
    request.state.user = None

    if request.url.path.startswith('/api'):
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
        return


register_tortoise(app, config=ORM)

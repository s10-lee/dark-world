from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.src.user.routers import router as api_user
# from app.src.grab.routers import router as api_grab
# from app.src.miro.routers import router as api_miro
from app.src.web.routers import web_router, web
from app.src.auth.services import auth_wrapper
from app.settings import ORM, CORS_ALLOW_ORIGINS, APP_PARAMS, DEBUG

app = FastAPI(**APP_PARAMS)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware('http')
async def get_current_user_middleware(request: Request, call_next):
    request.state.user = None

    try:
        auth_jwt = request.headers.get('authorization')
        user_data = await auth_wrapper(auth_jwt)
        request.state.user = {
            'id': user_data['sub'],
            'username': user_data['name'],
        }
    except Exception as e:
        print(str(e))

    return await call_next(request)

app.include_router(web_router)
app.include_router(api_user, prefix='/api')
# app.include_router(api_grab, prefix='/api/ws')
# app.include_router(api_miro, prefix='/api/miro')

app.mount('/', web)

if not DEBUG:
    @app.get("/redoc", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def get_docs():
        return


register_tortoise(app, config=ORM)

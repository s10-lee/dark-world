from fastapi import Request
from app.src.auth.services import auth_wrapper, security


# app = FastAPI()
# @app.middleware('http')
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

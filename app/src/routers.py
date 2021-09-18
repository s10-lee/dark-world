from fastapi import APIRouter
from app.src.user.routers import router as api_user
from app.src.link.routers import router as api_link

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(api_user)
api_router.include_router(api_link, prefix='/link')

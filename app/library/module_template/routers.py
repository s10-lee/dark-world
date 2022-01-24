from fastapi import APIRouter, Request, Depends
from app.library.routers import CRUDRouter
from app.src.user.models import User
from app.src.auth.services import auth_wrapper
# from app.src.{{NAME}}.models import Model
# from app.src.{{NAME}}.schemas import SchemaReceive, SchemaCreate, SchemaList


router = APIRouter(tags=[], prefix='/{{NAME}}')


# @router.get('/public-route/')
# async def public_route(request: Request):
#     return {'user': request.state.user}
#
#
# @router.get('/private-route/')
# async def private_route(user: User = Depends(auth_wrapper)):
#     return {'user': user}


# router_crud = CRUDRouter(
#     model=Dummy,
#     lookup_field='uid',
#     schema=SchemaReceive,
#     schema_in=SchemaCreate,
#     schema_list=SchemaList,
# )
# router.include_router(router_crud, prefix='/dummy')

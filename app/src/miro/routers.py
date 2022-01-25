from fastapi import APIRouter, Request, Depends
from app.library.routers import CRUDRouter
from app.src.user.models import User
from app.src.auth.services import auth_wrapper
from app.src.miro import schemas, models


router = APIRouter(tags=['Miro'])


# @router.get('/public-route/')
# async def public_route(request: Request):
#     return {'user': request.state.user}
#
#
# @router.get('/private-route/')
# async def private_route(user: User = Depends(auth_wrapper)):
#     return {'user': user}


router_board = CRUDRouter(
    model=models.Board,
    lookup_field='uid',
    schema=schemas.BoardSchemaReceive,
    schema_in=schemas.BoardSchemaCreate,
    schema_list=schemas.BoardSchemaList,
)
router.include_router(router_board, prefix='/board')


router_block = CRUDRouter(
    model=models.Block,
    lookup_field='uid',
    schema=schemas.BlockSchemaReceive,
    schema_in=schemas.BlockSchemaCreate,
    schema_list=schemas.BlockSchemaList,
)
router.include_router(router_board, prefix='/block')

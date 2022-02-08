from fastapi import APIRouter, Depends
from app.library.routers import CRUDRouter
from app.src.grab.models import Chain
from app.src.auth.services import auth_wrapper
from app.src.grab.schemas import (
    ChainSchemaCreate,
    ChainSchemaReceive,
    ChainSchemaList,
    # RequestSchemaCreate,
    # RequestSchemaReceive,
    # RequestSchemaList,
)

router = APIRouter(tags=['Web Scraping'])

router_chain = CRUDRouter(
    model=Chain,
    lookup_field='uid',
    schema=ChainSchemaReceive,
    schema_in=ChainSchemaCreate,
    schema_list=ChainSchemaList,
    dependencies=[Depends(auth_wrapper)],
    by_user=True,
)
router.include_router(router_chain, prefix='/chain')


# @router.get('/')
# async def list_items(user_id=Depends(get_current_user_id)):
#     try:
#         return await ChainSchemaList.from_queryset(Chain.filter(user_id=user_id))
#     except Exception as e:
#         raise HTTPException(400, str(e))


# router_request = CRUDRouter(
#     model=Request,
#     lookup_field='uid',
#     schema=RequestSchemaReceive,
#     schema_in=RequestSchemaCreate,
#     schema_list=RequestSchemaList,
# )
# router.include_router(router_request, prefix='/request')


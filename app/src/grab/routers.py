from fastapi import APIRouter
from app.library.routers import CRUDRouter
from app.src.grab.models import Project
from app.src.grab.schemas import (
    ProjectSchemaCreate,
    ProjectSchemaReceive,
    ProjectSchemaList,
    # RequestSchemaCreate,
    # RequestSchemaReceive,
    # RequestSchemaList,
)


router_project = CRUDRouter(
    model=Project,
    lookup_field='uid',
    schema=ProjectSchemaReceive,
    schema_in=ProjectSchemaCreate,
    schema_list=ProjectSchemaList,
)

router = APIRouter(tags=['Web Scraping'], prefix='/ws')
router.include_router(router_project, prefix='/project')


# router_request = CRUDRouter(
#     model=Request,
#     lookup_field='uid',
#     schema=RequestSchemaReceive,
#     schema_in=RequestSchemaCreate,
#     schema_list=RequestSchemaList,
# )
# router.include_router(router_request, prefix='/request')


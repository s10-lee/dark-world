from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.library.routers import CRUDRouter
from app.src.grab.models import Project, ProjectStep, User, Request
from app.src.grab.schemas import (
    CreateProject,
    ReceiveProject,
    ListProject,
    RequestSchemaCreate,
    RequestSchemaReceive,
    RequestSchemaList,
)
from app.src.auth.services import current_auth_user


router = APIRouter(tags=['Web Scraping'])


@router.get('/project/')
async def list_project(user: User = Depends(current_auth_user)) -> Optional[ListProject]:
    try:
        return await ListProject.from_queryset(Project.filter(user=user))
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post('/project/', response_model=ReceiveProject)
async def create_project(data: CreateProject, user: User = Depends(current_auth_user)) -> Optional[ReceiveProject]:
    try:
        return await Project.create(user=user, **data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get('/project/{uid}/', response_model=ReceiveProject)
async def receive_project(uid: UUID, user: User = Depends(current_auth_user)) -> Optional[ReceiveProject]:
    try:
        return await Project.get(uid=uid, user=user)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.delete('/project/{uid}/')
async def destroy_project(uid: UUID, user: User = Depends(current_auth_user)):
    obj = await Project.filter(uid=uid, user=user).delete()
    if not obj:
        raise HTTPException(404, 'Object does not exist')
    return obj


router_request = CRUDRouter(
    model=Request,
    lookup_field='uid',
    tags=['Request'],
    schema=RequestSchemaReceive,
    schema_in=RequestSchemaCreate,
    schema_list=RequestSchemaList,
)

# dependencies=[Depends(current_auth_user)]

router.include_router(router_request, prefix='/request')

# def create_crud_endpoint():
#     return {'CRUD': 'Yeeeessss!!'}
#
# router.add_api_route('/crud/', create_crud_endpoint)


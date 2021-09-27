from fastapi import Depends, APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from app.src.grab.models import Project, ProjectStep, User
from app.src.grab.schemas import CreateProject, ReceiveProject, ListProject
from app.src.auth.services import (
    validate_signup,
    authentication_user,
    client_token_response,
    auth_check_refresh,
    auth_wrapper,
    current_auth_user,
)


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
    return {'detail': 'Object was deleted'}


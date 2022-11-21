from fastapi import Depends, APIRouter, HTTPException
from tortoise.models import Q
from app.src.project import schemas, models
from app.src.auth.services import get_current_user_id
from uuid import UUID


router = APIRouter(tags=['Project'])

model = models.Project
url_path = '/project/'


@router.get(url_path)
async def list_items(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.List.from_queryset(
        model.filter(
            Q(access='all') | Q(Q(access='none') & Q(users__user=user_id))
        ),
    )


@router.get(url_path + '{code}/', response_model=schemas.Receive)
async def receive_item(code: str, user_id: UUID = Depends(get_current_user_id)):
    item = await model.filter(code=code).filter(
        Q(access='all') | Q(Q(access='none') & Q(users__user=user_id))
    ).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail={'message': 'Not Found'}
        )
    # await item.fetch_related('responses')
    return item


@router.post(url_path, response_model=schemas.Receive)
async def create_item(data: schemas.Create, user_id: UUID = Depends(get_current_user_id)):
    return await model.create(**data.dict(exclude_unset=True, exclude_none=True))


@router.patch(url_path + '{pk}/', response_model=schemas.Receive)
async def update_item(pk: int, data: schemas.Create, user_id: UUID = Depends(get_current_user_id)):
    item = await model.get(id=pk)
    await item.update_from_dict(data.dict(exclude_unset=True, exclude_none=True)).save()
    return item


@router.delete(url_path + '{pk}/')
async def delete_item(pk: int, user_id: UUID = Depends(get_current_user_id)):
    item = await model.get(id=pk)
    await item.delete()
    return {}

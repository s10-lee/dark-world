from fastapi import Depends, APIRouter
from app.library.web import parse_html_response, send_http_request
from app.src.scrape.models import Request, HttpMethod
from app.src.scrape import schemas
from app.src.auth.services import get_current_user_id
from uuid import UUID
import orjson

# ------------- #
#    Request    #
# ------------- #


router = APIRouter(tags=['HTTP Requests'])


@router.get('/ws-methods/')
async def list_methods(user_id: UUID = Depends(get_current_user_id)):
    return {item.name: item.value for item in HttpMethod}


@router.get('/ws-request/')
async def list_requests(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.RequestList.from_queryset(Request.filter(collection__user__id=user_id))


@router.get('/ws-request/{pk}/', response_model=schemas.RequestReceive)
async def receive_request(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    item = await Request.get(id=pk, collection__user__id=user_id)
    await item.fetch_related('responses')
    return item


@router.post('/ws-request/', response_model=schemas.RequestReceive)
async def create_request(data: schemas.RequestCreate, user_id: UUID = Depends(get_current_user_id)):
    return await Request.create(**data.dict(exclude_unset=True, exclude_none=True))


@router.put('/ws-request/{pk}/', response_model=schemas.RequestReceive)
async def update_request(pk: UUID, data: schemas.RequestCreate, user_id: UUID = Depends(get_current_user_id)):
    item = await Request.get(id=pk, collection__user__id=user_id).prefetch_related('responses')
    await item.update_from_dict(data.dict(exclude_unset=True, exclude_none=True)).save()
    return item


@router.delete('/ws-request/{pk}/')
async def delete_request(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    item = await Request.get(id=pk, collection__user__id=user_id)
    await item.delete()
    return {}

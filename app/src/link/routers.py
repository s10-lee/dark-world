from typing import Optional
from fastapi import Request, Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from .schemas import CreateSchema, ReceiveSchema
from .services import create, receive


router = APIRouter()


@router.post('/', response_model=ReceiveSchema)
async def create_item(data: CreateSchema) -> Optional[ReceiveSchema]:
    item = await create(**data.dict(exclude_unset=True))
    return item


# @router.get('/{code}', response_model=ReceiveSchema)
async def client_redirect(code: str) -> Optional[ReceiveSchema]:
    item = await receive(code)
    if not item:
        raise HTTPException(status_code=404)
    return RedirectResponse(item.url)

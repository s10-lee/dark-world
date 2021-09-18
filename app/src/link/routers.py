from typing import Optional
from fastapi import Request, Depends, APIRouter, HTTPException
from .schemas import CreateSchema, ReceiveSchema
from .services import create, receive


router = APIRouter()


@router.post('/', response_model=ReceiveSchema)
async def create_item(data: CreateSchema) -> Optional[ReceiveSchema]:
    item = await create(**data.dict(exclude_unset=True))
    return item


@router.get('/{code}', response_model=ReceiveSchema)
async def receive_item(code: str) -> Optional[ReceiveSchema]:
    item = await receive(code)
    if not item:
        raise HTTPException(404)
    return item


from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Collection, Request, Variable, Parser
from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional


class GrabberYoutubeSchema(BaseModel):
    url: HttpUrl
    itag: Optional[int] = None


class GrabberSchema(BaseModel):
    url: HttpUrl
    pattern: Optional[str] = None
    save: Optional[bool] = None
    update_id: Optional[UUID] = None


CollectionCreate = pydantic_model_creator(
    Collection,
    name='CollectionCreate',
    include=('name', 'position')
)

CollectionReceive = pydantic_model_creator(
    Collection,
    name='CollectionReceive',
    include=('id', 'name', 'position', 'requests', 'variables'),
    exclude_readonly=True,
)
CollectionList = pydantic_queryset_creator(
    Collection,
    name='CollectionList',
    exclude=('user', 'user_id', 'requests', 'variables'),
)


RequestCreate = pydantic_model_creator(
    Request,
    name='RequestCreate',
    exclude_readonly=True,
)
RequestReceive = pydantic_model_creator(
    Request,
    name='RequestReceive',
    exclude=('collection',),
    computed=('last_response',)
)
RequestList = pydantic_queryset_creator(
    Request,
    name='RequestList',
    exclude=('collection',),
)


VariableCreate = pydantic_model_creator(
    Variable,
    name='VariableCreate',
    exclude_readonly=True,
)
VariableReceive = pydantic_model_creator(
    Variable,
    name='VariableReceive',
    exclude_readonly=True,
)
VariableList = pydantic_queryset_creator(
    Variable,
    name='VariableList',
    exclude=('collection',),
)

ParserCreate = pydantic_model_creator(
    Parser,
    name='ParserCreate',
    exclude_readonly=True,
    exclude=('user', 'user_id'),
)
ParserReceive = pydantic_model_creator(
    Parser,
    name='ParserReceive',
    exclude=('user', 'user_id'),
    exclude_readonly=True,
)
ParserList = pydantic_queryset_creator(
    Parser,
    name='ParserList',
    exclude=('user', 'user_id'),
)

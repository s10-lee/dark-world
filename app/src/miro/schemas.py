from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.miro.models import Board, Block


BoardSchemaCreate = pydantic_model_creator(
    Board,
    name='BoardSchemaCreate',
    exclude_readonly=True,
)
BoardSchemaReceive = pydantic_model_creator(
    Board,
    name='BoardSchemaReceive',
    exclude=('id', ),
)
BoardSchemaList = pydantic_queryset_creator(
    Board,
    name='BoardSchemaList',
    exclude=('id', ),
)


BlockSchemaCreate = pydantic_model_creator(
    Block,
    name='BlockSchemaCreate',
    exclude_readonly=True,
)
BlockSchemaReceive = pydantic_model_creator(
    Block,
    name='BlockSchemaReceive',
    exclude=('id', ),
)
BlockSchemaList = pydantic_queryset_creator(
    Block,
    name='BlockSchemaList',
    exclude=('id', ),
)

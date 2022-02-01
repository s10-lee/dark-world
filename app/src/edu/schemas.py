from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.edu.models import Topic


SchemaCreate = pydantic_model_creator(
    Topic,
    name='SchemaCreate',
    exclude_readonly=True,
)
SchemaReceive = pydantic_model_creator(
    Topic,
    name='SchemaReceive',
    exclude=('id', ),
)

SchemaList = pydantic_queryset_creator(
    Topic,
    name='SchemaList',
    exclude=('id', ),
)

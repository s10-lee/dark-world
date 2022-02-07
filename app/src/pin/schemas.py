from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.pin.models import Pin
from pydantic import BaseModel, Field, HttpUrl


class PinSchemaGrab(BaseModel):
    url: HttpUrl


# SchemaCreate = pydantic_model_creator(
#     Model,
#     name='SchemaCreate',
#     exclude_readonly=True,
# )
PinSchemaReceive = pydantic_model_creator(
    Pin,
    name='PinSchemaReceive',
    exclude=('id', 'user', ),
    computed=('url', )
)

PinSchemaList = pydantic_queryset_creator(
    Pin,
    name='PinSchemaList',
    exclude=('id', 'user', ),
    computed=('url', ),
)

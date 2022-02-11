from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.gallery.models import Pin


# PinCreate = pydantic_model_creator(
#     Pin,
#     name='PinCreate',
#     exclude_readonly=True,
# )
PinReceive = pydantic_model_creator(
    Pin,
    name='PinReceive',
    exclude=('id', 'user', ),
    computed=('url', )
)

PinList = pydantic_queryset_creator(
    Pin,
    name='PinList',
    exclude=('id', 'user', ),
    computed=('url', ),
)

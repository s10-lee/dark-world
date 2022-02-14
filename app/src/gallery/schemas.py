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
    exclude=('user', 'user_id', 'deleted_at'),
    computed=('url', 'type')
)

PinList = pydantic_queryset_creator(
    Pin,
    name='PinList',
    exclude=('user', 'user_id', 'deleted_at'),
    computed=('url', 'type'),
)

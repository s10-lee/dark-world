from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.gallery.models import MediaItem
from pydantic import BaseModel, HttpUrl


class MediaItemGrab(BaseModel):
    url: HttpUrl


# SchemaCreate = pydantic_model_creator(
#     Model,
#     name='SchemaCreate',
#     exclude_readonly=True,
# )
MediaItemReceive = pydantic_model_creator(
    MediaItem,
    name='MediaItemReceive',
    exclude=('id', 'user', ),
    computed=('url', )
)

MediaItemList = pydantic_queryset_creator(
    MediaItem,
    name='MediaItemList',
    exclude=('id', 'user', ),
    computed=('url', ),
)

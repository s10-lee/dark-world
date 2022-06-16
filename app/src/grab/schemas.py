from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Collection
from pydantic import BaseModel, HttpUrl
from typing import Optional


class GrabberYoutubeSchema(BaseModel):
    url: HttpUrl
    itag: Optional[int] = None


class GrabberSchema(BaseModel):
    url: HttpUrl
    pattern: Optional[str] = None
    save: Optional[bool] = None
    # raw save


CollectionCreate = pydantic_model_creator(
    Collection,
    name='CollectionCreate',
    exclude_readonly=True,
)

CollectionReceive = pydantic_model_creator(
    Collection,
    name='CollectionReceive',
)


CollectionList = pydantic_queryset_creator(
    Collection,
    name='CollectionList',
    exclude=('user', 'user_id'),
)

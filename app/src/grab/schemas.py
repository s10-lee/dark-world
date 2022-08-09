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

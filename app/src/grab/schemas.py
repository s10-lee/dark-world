from pydantic import BaseModel, HttpUrl
from typing import Optional


class GrabberYoutubeSchema(BaseModel):
    url: HttpUrl
    itag: Optional[int] = None


class GrabberSchema(BaseModel):
    url: HttpUrl
    pattern: Optional[str] = None
    source: Optional[bool] = None
    save: Optional[bool] = None
    # raw save

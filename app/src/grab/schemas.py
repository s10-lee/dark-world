from pydantic import BaseModel, HttpUrl
from typing import Optional


class GrabberSchema(BaseModel):
    url: HttpUrl
    pattern: Optional[str] = None
    source: Optional[bool] = None
    save: Optional[bool] = None

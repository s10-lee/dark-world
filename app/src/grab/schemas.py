from pydantic import BaseModel, HttpUrl


class GrabUrl(BaseModel):
    url: HttpUrl

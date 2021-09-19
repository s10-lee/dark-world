from tortoise.contrib.pydantic import pydantic_model_creator
from .models import Link

CreateSchema = pydantic_model_creator(
    Link,
    name='CreateSchema',
    include=('url', ),
)

ReceiveSchema = pydantic_model_creator(
    Link,
    name='ReceiveSchema',
    include=('code', ),
)
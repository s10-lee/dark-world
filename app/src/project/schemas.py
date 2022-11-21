from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.project.models import Project

Create = pydantic_model_creator(
    Project,
    name='ProjectCreate',
)
Receive = pydantic_model_creator(
    Project,
    name='ProjectReceive',
    exclude_readonly=True,
)
List = pydantic_queryset_creator(
    Project,
    name='ProjectList',
    exclude=('users', )
)

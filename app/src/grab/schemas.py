from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Project, ProjectStep, Request
from typing import List, Type


RequestSchemaCreate = pydantic_model_creator(
    Request,
    name='RequestSchemaCreate',
    exclude=('id', 'is_active', 'slug', 'uid', 'user_id',),
    exclude_readonly=True,

)

RequestSchemaReceive = pydantic_model_creator(
    Request,
    name='RequestSchemaReceive',
    include=('name', 'method', 'url', 'params', 'headers', 'data', 'project_id', 'created_at', 'updated_at'),
)
RequestSchemaList = pydantic_queryset_creator(
    Request,
    name='RequestSchemaList',
    # exclude=('id', )
    include=('name', 'method', 'url', 'params', 'headers', 'data', 'project_id', 'created_at', 'updated_at'),
)


CreateProject = pydantic_model_creator(
    Project,
    name='CreateProject',
    exclude=('is_active', 'slug', 'uid'),
    exclude_readonly=True,
)

ReceiveProject = pydantic_model_creator(
    Project,
    name='ReceiveProject',
    exclude=('id', )
)


ListProject = pydantic_queryset_creator(Project, name='ListProject', exclude=('id', ))

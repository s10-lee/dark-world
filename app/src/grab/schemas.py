from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Project, ProjectStep
from typing import List


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

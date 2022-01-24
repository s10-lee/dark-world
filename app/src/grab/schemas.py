from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Project, ProjectStep
from typing import List, Type
from app.db.utils import init_models

# RequestSchemaCreate = pydantic_model_creator(
#     Request,
#     name='RequestSchemaCreate',
#     exclude=('id', 'is_active', 'slug', 'uid', 'user_id'),
#     exclude_readonly=True,
# )
# RequestSchemaReceive = pydantic_model_creator(
#     Request,
#     name='RequestSchemaReceive',
#     include=('uid', 'name', 'method', 'url', 'params', 'headers', 'data', 'project_id', 'created_at', 'updated_at'),
# )
# RequestSchemaList = pydantic_queryset_creator(
#     Request,
#     name='RequestSchemaList',
#     include=('uid', 'name', 'method', 'url', 'params', 'headers'),
# )
ProjectStepSchemaCreate = pydantic_model_creator(
    ProjectStep,
    name='ProjectStepSchemaCreate',
    exclude_readonly=True,
)

ProjectStepSchemaReceive = pydantic_model_creator(
    ProjectStep,
    name='ProjectStepSchemaReceive',
    exclude=('id', ''),
)


ProjectSchemaCreate = pydantic_model_creator(
    Project,
    name='ProjectSchemaCreate',
    exclude_readonly=True,
)
ProjectSchemaReceive = pydantic_model_creator(
    Project,
    name='ProjectSchemaReceive',
    exclude=('id', ),
)
ProjectSchemaList = pydantic_queryset_creator(
    Project,
    name='ProjectSchemaList',
    exclude=('id', 'steps'),
)

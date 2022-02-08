from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel
from app.src.grab.models import Chain, Step

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
# ChainStepSchemaCreate = pydantic_model_creator(
#     ChainStep,
#     name='ChainStepSchemaCreate',
#     exclude_readonly=True,
# )
#
# ChainStepSchemaReceive = pydantic_model_creator(
#     ChainStep,
#     name='ChainStepSchemaReceive',
#     exclude=('id', ''),
# )
#


StepSchemaList = pydantic_queryset_creator(
    Step,
    name='StepSchemaList',
    include=('uid', 'name', 'object_id', 'object_type'),
)

ChainSchemaCreate = pydantic_model_creator(
    Chain,
    name='ChainSchemaCreate',
    include=('name', ),
    exclude_readonly=True,

)
ChainSchemaReceive = pydantic_model_creator(
    Chain,
    name='ChainSchemaReceive',
    include=('uid', 'name', 'steps'),
    exclude=('steps.lft', 'steps.rgt', 'steps.id', 'steps.user', 'steps.user_id'),
)
ChainSchemaList = pydantic_queryset_creator(
    Chain,
    name='ChainSchemaList',
    exclude=('id', 'user', 'steps'),
)



from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.src.grab.models import Chain

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

ChainSchemaUpdate = pydantic_model_creator(
    Chain,
    name='ChainSchemaUpdate',
    exclude_readonly=True,
    # exclude=('id', 'user', ),
)

ChainSchemaCreate = pydantic_model_creator(
    Chain,
    name='ChainSchemaCreate',
    exclude_readonly=True,
    include=('name', )
)
ChainSchemaReceive = pydantic_model_creator(
    Chain,
    name='ChainSchemaReceive',
    exclude=('id', 'user'),
)
ChainSchemaList = pydantic_queryset_creator(
    Chain,
    name='ChainSchemaList',
    exclude=('id', 'user'),
)

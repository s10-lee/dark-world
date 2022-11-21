from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import MODEL


def create_model_schemas(model_class: MODEL, **kwargs):
    create_schema = pydantic_model_creator(
        model_class,
        name=model_class.__class__.__name__ + 'Create',
        include=kwargs.get('create_include'),
        exclude=kwargs.get('create_exclude'),
        exclude_readonly=kwargs.get('create_exclude_readonly'),
    )
#
# Receive = pydantic_model_creator(
#     Project,
#     name='ProjectReceive',
#     exclude_readonly=True,
# )
# List = pydantic_queryset_creator(
#     Project,
#     name='ProjectList',
# )

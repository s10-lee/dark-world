from tortoise import fields, Model
from tortoise.exceptions import NoValuesFetched
from app.db.fields import UUIDField
from app.src.user.models import User
from app.library.web import convert_data_to_json, convert_json_to_dict
from typing import Union
from app.db.utils import init_models
from enum import Enum
from uuid import uuid4


class HttpMethod(str, Enum):
    HEAD = 'HEAD'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'


class Collection(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='collections',
        on_delete=fields.CASCADE,
    )
    steps: fields.ReverseRelation['Step']
    # requests: fields.ReverseRelation['Request']
    variables: fields.ReverseRelation['Variable']

    class Meta:
        table = 'ws_collection'


class Step(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255, null=True)
    type = fields.CharField(255, default='request')
    entity_id = fields.IntField(index=True)
    parent: fields.ForeignKeyNullableRelation['Step'] = fields.ForeignKeyField(
        'models.Step',
        related_name='children',
        null=True,
    )
    children: fields.ReverseRelation['Step']
    collection: fields.ForeignKeyRelation[Collection] = fields.ForeignKeyField(
        'models.Collection',
        related_name='steps',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'ws_collection_step'


class Request(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255, null=True)
    method: HttpMethod = fields.CharEnumField(HttpMethod, default=HttpMethod.GET)
    url = fields.CharField(500)
    params = fields.JSONField(null=True)
    headers = fields.JSONField(null=True)
    data = fields.TextField(null=True)
    cookies = fields.TextField(null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='requests',
        on_delete=fields.CASCADE,
    )
    responses: fields.ReverseRelation['HttpCall']

    def last_response(self) -> Union[str, dict, None]:
        try:
            resp = self.responses.related_objects[-1]
            data = convert_json_to_dict(resp.data)
            data['id'] = resp.id
            return data
        except (NoValuesFetched, IndexError):
            return None

    class Meta:
        table = 'ws_request'


class HttpCall(Model):
    id = fields.IntField(pk=True)
    method = fields.CharField(10)
    url = fields.CharField(500)
    request_headers = fields.TextField(null=True)
    request_body = fields.TextField(null=True)
    status = fields.IntField(null=True)
    response_headers = fields.TextField(null=True)
    response_body = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    request: fields.ForeignKeyRelation[Request] = fields.ForeignKeyField(
        'models.Request',
        related_name='responses',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'ws_http_call'


class Parser(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255, null=True)
    content_type = fields.CharField(50, null=False, default='text/html')
    search_field = fields.CharField(255, default='body')
    search_pattern = fields.CharField(255)
    element_index = fields.IntField(null=True)
    action = fields.CharField(255, null=True)
    action_args = fields.JSONField(null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='parsers',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'ws_parser'


class Variable(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255)
    value = fields.TextField(default='')
    call = fields.CharField(255, null=True)
    collection: fields.ForeignKeyRelation[Collection] = fields.ForeignKeyField(
        'models.Collection',
        related_name='variables',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'ws_variable'


init_models(['app.src.scrape.models'])

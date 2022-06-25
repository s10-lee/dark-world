from tortoise import fields, Model
from tortoise.exceptions import NoValuesFetched
from app.db.models import DateTimeMixin
from app.db.fields import UUIDField
from app.src.user.models import User
from app.library.web import convert_data_to_json, convert_json_to_dict
from app.settings import MEDIA_URL
from typing import Union
from app.db.utils import init_models
from enum import Enum


class HttpMethod(str, Enum):
    HEAD = 'HEAD'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'


class HttpHeader(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255, unique=True)
    in_request = fields.BooleanField(default=False)
    in_response = fields.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        table = 'http_header'


class Collection(Model):
    id = UUIDField(pk=True)
    name = fields.CharField(255)
    position = fields.SmallIntField(default=1)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        on_delete=fields.CASCADE,
    )
    requests: fields.ReverseRelation['Request']
    variables: fields.ReverseRelation['Variable']

    class Meta:
        ordering = ('position',)
        table = 'http_collection'


class Request(Model):
    id = UUIDField(pk=True)
    method: HttpMethod = fields.CharEnumField(HttpMethod, default=HttpMethod.GET)
    url = fields.CharField(500)
    params = fields.JSONField(default=list, null=True)
    headers = fields.JSONField(default=list, null=True)
    data = fields.TextField(default='', null=True)
    cookies = fields.TextField(null=True)
    cert = fields.BinaryField(null=True)

    position = fields.SmallIntField(default=1)
    collection: fields.ForeignKeyRelation[Collection] = fields.ForeignKeyField(
        'models.Collection',
        related_name='requests',
        on_delete=fields.CASCADE,
    )
    responses: fields.ReverseRelation['Response']

    def last_response(self) -> Union[str, dict, None]:
        try:
            return convert_json_to_dict(self.responses.related_objects[-1].data)
        except (NoValuesFetched, IndexError):
            return None

    class Meta:
        ordering = ('position',)
        table = 'http_request'


class Response(Model):
    id = fields.IntField(pk=True)
    data = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    request: fields.ForeignKeyRelation[Request] = fields.ForeignKeyField(
        'models.Request',
        related_name='responses',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'http_response'


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
        table = 'http_variable'


#
# Pinterest
#   //img[@data-animated-url]/@data-animated-url
#
# Dribble
#   //meta[@property="og:image"]/@content
#   //img[@data-test="v-img"]/@src
#
class Grabber(Model):
    id = UUIDField(pk=True)
    name = fields.CharField(255)
    icon = fields.CharField(255)
    type = fields.CharField(50, null=False, default='html')
    patterns = fields.JSONField(default=list)
    search_xpath = fields.CharField(255)
    element_index = fields.IntField(null=True)

    class Meta:
        table = 'grabber'


init_models(['app.src.grab.models'])


from tortoise import fields, Model
from app.db.models import DateTimeMixin
from app.db.fields import UUIDField
from app.src.user.models import User
from app.settings import MEDIA_URL
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

# class Settings(Model):
#     id = fields.IntField(pk=True)


class Collection(Model):
    id = UUIDField(pk=True)
    name = fields.CharField(255)
    position = fields.SmallIntField(default=1)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        on_delete=fields.CASCADE,
    )

    class Meta:
        ordering = ('position',)
        table = 'http_collection'
#
#
# class Request(Model):
#     id = UUIDField(pk=True)
#     method: METHOD = fields.CharEnumField(METHOD, default=METHOD.GET)
#     url = fields.TextField()
#     params = fields.JSONField(default=dict)
#     headers = fields.JSONField(default=dict)
#     data = fields.JSONField(default=dict)
#     json = fields.JSONField(default=dict)
#     body = fields.BinaryField(null=True)
#     collection: fields.ForeignKeyRelation[Collection] = fields.ForeignKeyField(
#         'models.Collection',
#         on_delete=fields.CASCADE,
#     )
#
#     class Meta:
#         table = 'api_request'


# Pinterest
# //img[@data-test="v-img"]/@src
# //img[@data-animated-url]/@data-animated-url
# Dribble
# //img[@data-test="v-img"]/@src
# class Grabber(DateTimeMixin):
#     id = UUIDField(pk=True)
#     name = fields.CharField(255)
#     icon = fields.CharField(255)
#     type = fields.CharField(50, null=False, default='html')
#     patterns = fields.JSONField(default=list)
#     search_xpath = fields.CharField(255)
#     element_index = fields.IntField(null=True)
#
#     class Meta:
#         table = 'grabber'
#


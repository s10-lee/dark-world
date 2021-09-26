from tortoise.models import Model
from tortoise.fields import (
    IntField,
    CharField,
    DatetimeField,
    CharEnumField,
    TextField,
    JSONField,
    ForeignKeyField,
    ForeignKeyRelation,
    ForeignKeyNullableRelation,
    ReverseRelation,
)
from app.db.fields import IPAddressField, UUIDField
from app.src.user.models import User
from enum import Enum


class METHODS(str, Enum):
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class GrabberProject(Model):
    id = IntField(pk=True)
    slug = CharField(50, unique=True)
    name = CharField(200, default='')
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    requests: ReverseRelation['GrabberRequest']
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    class Meta:
        table = 'grab_project'


class GrabberRequest(Model):
    id = IntField(pk=True)
    name = CharField(200, default='')
    method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
    url = CharField(255)
    params = JSONField(null=True)
    headers = JSONField(null=True)
    data = JSONField(null=True)

    project: ForeignKeyRelation[GrabberProject] = ForeignKeyField('models.GrabberProject', 'requests')
    parent: ForeignKeyNullableRelation["GrabberRequest"] = ForeignKeyField(
        'models.GrabberRequest', related_name="children", null=True
    )
    children: ReverseRelation['GrabberRequest']

    class Meta:
        table = 'grab_request'


class GrabberResponse(Model):
    id = IntField(pk=True)
    request: ForeignKeyRelation[GrabberRequest] = ForeignKeyField('models.GrabberRequest', 'responses')
    headers = JSONField(null=True)
    status = IntField(null=True)
    data = TextField(null=True)
    json = JSONField(null=True)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id", )
        table = 'grab_request_response'

# class Proxy(Model):
#     id = UUIDField(pk=True)
#     host = IPAddressField(unique=True)
#     port = IntField()
#     updated_at = DatetimeField(auto_now=True)
#
#     class Meta:
#         table = 'proxy'

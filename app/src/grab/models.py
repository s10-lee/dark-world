from tortoise.fields import (
    IntField,
    CharField,
    DatetimeField,
    CharEnumField,
    BooleanField,
    TextField,
    JSONField,
    ForeignKeyField,
    ForeignKeyRelation,
    ForeignKeyNullableRelation,
    ReverseRelation,
    OneToOneField,
    OneToOneRelation,
    BackwardOneToOneRelation,
    SmallIntField,
    CASCADE,
)
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from enum import Enum
from app.db.utils import init_models


class TYPES(str, Enum):
    JSON = 'json'
    XML = 'xml'
    HTML = 'html'
    CSS = 'css'
    JS = 'js'


class METHODS(str, Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseModel(PrimaryKeyMixin):
    class Meta:
        abstract = True


# *************************************
#               Models
# *************************************

class Chain(BaseModel):
    name = CharField(255, default='')
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    steps: ReverseRelation['Step']

    class Meta:
        ordering = ('-id', )
        table = 'ws_chain'


class Request(BaseModel):
    method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
    url = CharField(255)
    params = JSONField(null=True)
    headers = TextField(null=True)
    data = JSONField(null=True)
    cert = CharField(255, null=True)
    chain: ForeignKeyRelation[Chain] = ForeignKeyField('models.Chain', 'requests')
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    # step: OneToOneRelation[Step] = OneToOneField(
    #     'models.Step', on_delete=CASCADE, related_name='request', pk=True
    # )

    class Meta:
        table = 'ws_request'


# class Parser(BaseModel):
#     search = CharField(255)
#     convert_from: TYPES = CharEnumField(TYPES, default=TYPES.JSON)
#     chain: ForeignKeyRelation[Chain] = ForeignKeyField('models.Chain', 'parsers')
#     user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
#
#     class Meta:
#         table = 'ws_parser'


class Step(BaseModel):
    name = CharField(255, default='')
    lft = IntField(null=True)
    rgt = IntField(null=True)
    level = IntField(default=0)
    object_id = IntField()
    object_type = CharField(255)
    chain: ForeignKeyRelation[Chain] = ForeignKeyField('models.Chain', 'steps')
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User')

    class Meta:
        ordering = ('level', 'id', )
        table = 'ws_chain_step'


# class HttpRequestResponse(PrimaryKeyMixin):
#     method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
#     url = CharField(500)
#     headers = JSONField(null=True)
#     data = TextField(null=True)
#     status = IntField(null=True)
#     response_headers = JSONField(null=True)
#     response_body = TextField(null=True)
#     request_at = DatetimeField(null=True)
#     response_at = DatetimeField(null=True)
#
#     chain: ForeignKeyRelation[Chain] = ForeignKeyField('models.Chain', 'http')
#     step: ForeignKeyRelation[ChainStep] = ForeignKeyField('models.ChainStep', 'http')
#
#     class Meta:
#         ordering = ("-id", )
#         table = 'ws_http'


init_models(['app.src.grab.models'])

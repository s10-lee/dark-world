from tortoise.models import Model
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
    SmallIntField,
)
from app.db.fields import IPAddressField, UUIDField
from uuid import uuid4
from app.src.user.models import User
from enum import Enum
from app.src.functions import init_models



class TYPES(str, Enum):
    JSON = "json"
    XML = "xml"
    HTML = "html"


class METHODS(str, Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class PkMixin(Model):
    id = IntField(pk=True)
    uid = UUIDField(default=uuid4, unique=True)

    class Meta:
        abstract = True


class DTMixin(Model):
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(PkMixin, DTMixin):
    class Meta:
        abstract = True


class NameSlugActiveMixin(Model):
    name = CharField(255, default='')
    slug = CharField(50, unique=True, null=True)
    is_active = BooleanField(default=True)

    class Meta:
        abstract = True


class Project(BaseModel, NameSlugActiveMixin):
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    requests: ReverseRelation['Request']
    parsers: ReverseRelation['Parser']
    steps: ReverseRelation['ProjectStep']

    class Meta:
        table = 'ws_project'


class ProjectStep(BaseModel, NameSlugActiveMixin):
    lft = IntField(null=True)
    rgt = IntField(null=True)
    level = IntField(default=0)
    position = IntField(default=0)
    project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'steps')
    parent: ForeignKeyNullableRelation['ProjectStep'] = ForeignKeyField(
        'models.ProjectStep', related_name="children", null=True
    )
    children: ReverseRelation['ProjectStep']


    class Meta:
        table = 'ws_project_step'


class Request(BaseModel, NameSlugActiveMixin):
    method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
    url = CharField(255)
    params = JSONField(null=True)
    headers = JSONField(null=True)
    data = JSONField(null=True)
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User', 'requests')
    project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'requests')

    class Meta:
        table = 'ws_request'


class Parser(BaseModel, NameSlugActiveMixin):
    search_rule = CharField(255)
    search_keys = JSONField(null=True)
    global_vars = JSONField(null=True)
    convert_from: TYPES = CharEnumField(TYPES, default=TYPES.JSON)
    single = BooleanField(default=False)
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User', 'parsers')
    project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'parsers')

    class Meta:
        table = 'ws_parser'


class HttpRequestResponse(PkMixin):
    method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
    url = CharField(500)
    headers = JSONField(null=True)
    data = TextField(null=True)
    status = IntField(null=True)
    response_headers = JSONField(null=True)
    response_body = TextField(null=True)
    request_at = DatetimeField(null=True)
    response_at = DatetimeField(null=True)

    project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'http')
    step: ForeignKeyRelation[ProjectStep] = ForeignKeyField('models.ProjectStep', 'http')

    class Meta:
        ordering = ("-id", )
        table = 'ws_http'

# class Proxy(Model):
#     id = UUIDField(pk=True)
#     host = IPAddressField(unique=True)
#     port = IntField()
#     updated_at = DatetimeField(auto_now=True)
#
#     class Meta:
#         table = 'proxy'


init_models(['app.src.grab.models'])

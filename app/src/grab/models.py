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
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from enum import Enum
from app.db.utils import init_models


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


class BaseModel(PrimaryKeyMixin):
    class Meta:
        abstract = True


# *************************************
#               Models
# *************************************


class ProjectStep(BaseModel):
    name = CharField(255, default='')
    lft = IntField(null=True)
    rgt = IntField(null=True)
    level = IntField(default=0)
    project: ForeignKeyRelation['Project'] = ForeignKeyField('models.Project', 'steps')
    # parent: ForeignKeyNullableRelation['ProjectStep'] = ForeignKeyField(
    #     'models.ProjectStep', related_name="children", null=True
    # )
    # children: ReverseRelation['ProjectStep']

    class Meta:
        table = 'ws_project_step'

    # class PydanticMeta:
    #     exclude = ('children', 'parent')


class Project(BaseModel):
    name = CharField(255, default='')
    # user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    # requests: ReverseRelation['Request']
    # parsers: ReverseRelation['Parser']
    steps: ReverseRelation[ProjectStep]

    class Meta:
        table = 'ws_project'


# class Request(BaseModel):
#     method: METHODS = CharEnumField(METHODS, default=METHODS.GET)
#     url = CharField(255)
#     params = JSONField(null=True)
#     headers = JSONField(null=True)
#     data = JSONField(null=True)
#     user: ForeignKeyRelation[User] = ForeignKeyField('models.User', 'requests')
#     project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'requests')
#
#     class Meta:
#         table = 'ws_request'


# class Parser(BaseModel):
#     search_rule = CharField(255)
#     search_keys = JSONField(null=True)
#     global_vars = JSONField(null=True)
#     convert_from: TYPES = CharEnumField(TYPES, default=TYPES.JSON)
#     single = BooleanField(default=False)
#     user: ForeignKeyRelation[User] = ForeignKeyField('models.User', 'parsers')
#     project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'parsers')
#
#     class Meta:
#         table = 'ws_parser'


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
#     project: ForeignKeyRelation[Project] = ForeignKeyField('models.Project', 'http')
#     step: ForeignKeyRelation[ProjectStep] = ForeignKeyField('models.ProjectStep', 'http')
#
#     class Meta:
#         ordering = ("-id", )
#         table = 'ws_http'


init_models(['app.src.grab.models'])

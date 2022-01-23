from tortoise import fields, Model
from app.db.models import PrimaryKeyMixin, DateTimeMixin
from app.src.user.models import User
from enum import Enum
from app.db.utils import init_models


class TYPES(str, Enum):
    JS = "js"
    CSS = "css"
    HTML = "html"


class Domain(PrimaryKeyMixin):
    url = fields.CharField(255)
    codes: fields.ReverseRelation['Code']

    class Meta:
        table = 'dw_domain'


class Code(PrimaryKeyMixin):
    name = fields.CharField(255)
    content = fields.TextField()
    code_type: TYPES = fields.CharEnumField(TYPES, default=TYPES.CSS)
    domain: fields.ForeignKeyRelation[Domain] = fields.ForeignKeyField('models.Domain', 'codes')

    class Meta:
        table = 'dw_domain_code'


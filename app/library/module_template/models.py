from tortoise import fields
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.db.utils import init_models


class Model(PrimaryKeyMixin):
    pass


init_models(['app.src.{{NAME}}.models'])

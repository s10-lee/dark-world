from tortoise import fields
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin
from app.src.user.models import User
from app.db.utils import init_models


class Model(PrimaryKeyMixin):
    # user: ForeignKeyRelation[User] = ForeignKeyField('models.User')
    pass


init_models(['app.src.{{NAME}}.models'])

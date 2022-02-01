from tortoise import fields
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from app.db.utils import init_models


# class Chapter(PrimaryKeyMixin):
#     name = fields.CharField(255)
#     body = fields.TextField()
#     user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', 'chapters')


class Topic(PrimaryKeyMixin):
    name = fields.CharField(255)
    body = fields.TextField()
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', 'topics')


init_models(['app.src.edu.models'])

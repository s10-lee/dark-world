from tortoise import fields
from app.db.models import DateTimeMixin
from app.db.fields import UUIDField
from app.src.user.models import User
from app.settings import MEDIA_URL
from app.db.utils import init_models
from enum import Enum


class Board(DateTimeMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(255)
    slug = fields.CharField(50, null=False, index=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')

    class Meta:
        unique_together = ('user', 'slug')
        table = 'gallery_board'


class Pin(DateTimeMixin):

    class TYPES(str, Enum):
        IMAGE = 'image'
        VIDEO = 'video'
        AUDIO = 'audio'

    id = UUIDField(pk=True)
    name = fields.CharField(255, blank=True)
    description = fields.TextField(blank=True, default='')
    extension = fields.CharField(50, blank=True)
    type: TYPES = fields.CharEnumField(TYPES, default=TYPES.IMAGE)

    gallery: fields.ForeignKeyNullableRelation[Board] = fields.ForeignKeyField(
        'models.Board',
        on_delete=fields.SET_NULL,
        null=True,
    )
    user: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField(
        'models.User',
        on_delete=fields.SET_NULL,
        null=True,
    )
    deleted_at = fields.DatetimeField(null=True)

    def url(self) -> str:
        return f'{MEDIA_URL}/{self.user_id}/{self.pk}.{self.extension}'

    class Meta:
        table = 'gallery_pin'


# class Tag(models.Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(50)
#     slug = fields.CharField(50, unique=True)
#     pins: fields.ManyToManyRelation['Pin'] = fields.ManyToManyField(
#         'models.Pin',
#         related_name='tags',
#         through='gallery_pin_tag',
#     )
#
#     class Meta:
#         table = 'gallery_tag'
#
#

init_models(['app.src.gallery.models'])

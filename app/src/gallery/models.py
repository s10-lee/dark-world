from tortoise import fields
from app.db.models import DateTimeMixin
from app.db.fields import UUIDKeyUnique
from app.src.user.models import User
from app.settings import MEDIA_URL
from app.db.utils import init_models
from enum import Enum


class TYPES(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class Gallery(DateTimeMixin):
    name = fields.CharField(255)
    slug = fields.CharField(50)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')

    class Meta:
        unique_together = ('user', 'slug')
        table = 'gallery'


class MediaItem(DateTimeMixin):
    id = fields.IntField(pk=True)
    uid = UUIDKeyUnique()
    title = fields.CharField(255, blank=True)
    extension = fields.CharField(10)
    type: TYPES = fields.CharEnumField(TYPES, default=TYPES.IMAGE)
    gallery: fields.ForeignKeyNullableRelation[Gallery] = fields.ForeignKeyField(
        'models.Gallery',
        on_delete=fields.SET_NULL,
        null=True,
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')

    def url(self) -> str:
        return f'{MEDIA_URL}/{self.user_id}/{self.pk}.{self.extension}'

    class Meta:
        table = 'gallery_media_item'


# init_models(['app.src.gallery.models'])

from tortoise import fields
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from app.settings import MEDIA_URL
from app.db.utils import init_models
from enum import Enum


class TYPES(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Board(PrimaryKeyMixin, DateTimeMixin):
    name = fields.CharField(255)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')

    class Meta:
        table = 'pin_board'


class Pin(PrimaryKeyMixin, DateTimeMixin):
    name = fields.CharField(255, blank=True)
    extension = fields.CharField(10)
    type: TYPES = fields.CharEnumField(TYPES, default=TYPES.IMAGE)
    board: fields.ForeignKeyNullableRelation[Board] = fields.ForeignKeyField(
        'models.Board',
        on_delete=fields.SET_NULL,
        null=True,
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')

    def url(self) -> str:
        return f'{MEDIA_URL}/{self.user_id}/{self.uid}.{self.extension}'

    class Meta:
        table = 'pin_item'


init_models(['app.src.pin.models'])

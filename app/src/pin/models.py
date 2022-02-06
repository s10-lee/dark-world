from tortoise import fields
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from app.db.utils import init_models


class Board(PrimaryKeyMixin, DateTimeMixin):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')
    name = fields.CharField(255)

    class Meta:
        table = 'pin_board'


class Pin(PrimaryKeyMixin, DateTimeMixin):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')
    name = fields.CharField(255, blank=True)
    board: fields.ForeignKeyNullableRelation[Board] = fields.ForeignKeyField(
        'models.Board',
        on_delete=fields.SET_NULL,
        null=True,
    )

    class Meta:
        table = 'pin_item'


init_models(['app.src.pin.models'])

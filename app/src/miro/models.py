from tortoise import fields
from app.db.fields import IPAddressField, UUIDField
from app.db.models import PrimaryKeyMixin, DateTimeMixin, NameSlugActiveMixin
from app.src.user.models import User
from app.db.utils import init_models


class Board(PrimaryKeyMixin):
    name = fields.CharField(255)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')
    is_public = fields.BooleanField(default=False)
    blocks: fields.ReverseRelation['Block']

    class Meta:
        table = 'miro_board'


class Block(PrimaryKeyMixin):
    name = fields.CharField(255)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User')
    board: fields.ForeignKeyRelation[Board] = fields.ForeignKeyField('models.Board', 'blocks')
    css = fields.CharField(255, default='')
    x = fields.IntField()
    y = fields.IntField()

    class Meta:
        table = 'miro_block'


init_models(['app.src.miro.models'])

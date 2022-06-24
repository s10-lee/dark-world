from tortoise.models import Model
from tortoise.fields import (
    IntField, CharField, ForeignKeyField, BooleanField, DatetimeField, ForeignKeyRelation
)
from app.db.fields import UUIDField
from datetime import datetime


class RefreshToken(Model):
    id = IntField(pk=True)
    user: ForeignKeyRelation['User'] = ForeignKeyField('models.User',  related_name='tokens')
    token = CharField(max_length=64, null=False)
    created_at = DatetimeField(auto_now_add=True)
    expires_at = DatetimeField(null=True)

    def expires(self):
        delta = self.expires_at - self.created_at
        return round(delta.total_seconds())

    class Meta:
        table = 'user_refresh_token'


class User(Model):
    id = UUIDField(pk=True)
    email = CharField(max_length=100, unique=True, null=False)
    username = CharField(max_length=50, unique=True, null=True)
    password = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    last_login = DatetimeField(null=True)

    async def logged(self):
        self.last_login = datetime.utcnow()
        await self.save()

    def __str__(self):
        return self.id

    class Meta:
        table = 'user'

    class PydanticMeta:
        pass

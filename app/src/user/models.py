from tortoise import Tortoise
from tortoise.models import Model
from tortoise.fields import (
    IntField, UUIDField, CharField, ForeignKeyField, BooleanField, DatetimeField, ManyToManyField,
    ManyToManyRelation, ForeignKeyRelation
)
from datetime import datetime


class Permission(Model):
    id = IntField(pk=True)
    slug = CharField(max_length=60)
    users: ManyToManyRelation['User'] = ManyToManyField(
        'models.User',
        related_name='perms',
        through='user_permission'
    )

    class Meta:
        table = 'permission'


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
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)
    email = CharField(max_length=100, unique=True, null=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    last_login = DatetimeField(null=True)
    perms: ManyToManyRelation[Permission]

    async def logged(self):
        self.last_login = datetime.utcnow()
        await self.save()

    def __str__(self):
        return self.username

    class Meta:
        table = 'user'



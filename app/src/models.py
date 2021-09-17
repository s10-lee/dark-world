from tortoise import Tortoise
from typing import Any
from tortoise.models import Model
from tortoise.fields import (
    IntField, UUIDField, CharField, ForeignKeyField, BooleanField, DatetimeField, ManyToManyField,
    ManyToManyRelation, ForeignKeyRelation, CASCADE, TextField
)
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime


class APIKeys(Model):
    id = IntField(pk=True)
    public_key = TextField()
    private_key = TextField()
    created_at = DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.created_at}'

    class Meta:
        table = 'key_pair'
        ordering = ('-id',)


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


class User(Model):
    id = UUIDField(pk=True)
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)
    email = CharField(max_length=200, default='')
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    last_login = DatetimeField(null=True, auto_now_add=True)
    perms: ManyToManyRelation[Permission]

    async def logged(self):
        self.last_login = datetime.utcnow()
        await self.save()

    def __str__(self):
        return self.username

    class Meta:
        table = 'user'


UserCredentials = pydantic_model_creator(
    User, 
    name='UserCredentials', 
    include=('username', 'password')
)


class SignUpToken(Model):
    id = UUIDField(pk=True)
    created_at = DatetimeField(auto_now_add=True)
    expires_at = DatetimeField(null=True)
    activated_at = DatetimeField(null=True)

    class Meta:
        table = 'user_signup_token'


class RefreshToken(Model):
    id = IntField(pk=True)
    user: ForeignKeyRelation[User] = ForeignKeyField(
        'models.User', 
        related_name='tokens', 
        on_delete=CASCADE,
    )
    token = CharField(max_length=64, null=False)
    created_at = DatetimeField(auto_now_add=True)
    expires_at = DatetimeField(null=True)

    def expires(self):
        delta = self.expires_at - self.created_at
        return round(delta.total_seconds())

    class Meta:
        table = 'user_refresh_token'


# Tortoise.init_models(['app.src.models'], 'models')

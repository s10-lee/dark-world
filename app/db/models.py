# from tortoise import Model, fields
from tortoise import models, fields
from tortoise.queryset import QuerySet, QuerySetSingle
from typing import TypeVar
from app.db.fields import UUIDField

MODEL = TypeVar("MODEL", bound="Model")


class Model(models.Model):
    pass


class DateTimeMixin(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class PrimaryKeyMixin(Model):
    id = fields.IntField(pk=True)
    uid = UUIDField(unique=True)

    class Meta:
        abstract = True


class NameSlugActiveMixin(Model):
    name = fields.CharField(255, default='')
    slug = fields.CharField(50, unique=True, null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        abstract = True


# class Aerich(Model):
#     version = fields.CharField(max_length=255)
#     app = fields.CharField(max_length=20)
#     content = fields.JSONField()
#
#     class Meta:
#         ordering = ["-id"]

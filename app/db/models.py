# from tortoise import Model, fields
from tortoise import models
# from tortoise.models import MODEL
from tortoise.queryset import QuerySet, QuerySetSingle
from typing import TypeVar

MODEL = TypeVar("MODEL", bound="Model")


class Model(models.Model):
    pass

# class Aerich(Model):
#     version = fields.CharField(max_length=255)
#     app = fields.CharField(max_length=20)
#     content = fields.JSONField()
#
#     class Meta:
#         ordering = ["-id"]

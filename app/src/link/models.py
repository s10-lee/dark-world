from tortoise.models import Model
from tortoise.fields import UUIDField, CharField, DatetimeField, BooleanField


class Link(Model):
    id = UUIDField(pk=True)
    url = CharField(max_length=255)
    code = CharField(max_length=50, unique=True)
    is_active = BooleanField(default=True)
    updated_at = DatetimeField(auto_now=True)
    created_at = DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = 'link'

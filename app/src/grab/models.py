from tortoise import fields, Model
from app.db.models import DateTimeMixin
from app.db.fields import UUIDField
from app.src.user.models import User
from app.settings import MEDIA_URL
from app.db.utils import init_models
from enum import Enum


# //img[@data-test="v-img"]/@src
# //img[@data-animated-url]/@data-animated-url
class Grabber(DateTimeMixin):
    id = UUIDField(pk=True)
    name = fields.CharField(255)
    icon = fields.CharField(255)
    type = fields.CharField(50, null=False, default='html')
    patterns = fields.JSONField(default=list)
    search_xpath = fields.CharField(255)
    element_index = fields.IntField(null=True)

    class Meta:
        table = 'grabber'


from tortoise import fields, Model
from app.db.models import DateTimeMixin
from app.db.fields import UUIDField
from app.src.user.models import User
from app.settings import MEDIA_URL
from app.db.utils import init_models
from enum import Enum


class Grabber(DateTimeMixin):
    id = UUIDField(pk=True)

    # Dribble
    name = fields.CharField(255)

    # MEDIA_URL / grabber / icons /
    icon = fields.CharField(255)

    # https://dribbble.com/shots/([-a-zA-Z_0-9]+)(/?)
    url_mask = fields.CharField(50, null=False, index=True)

    # //img[@data-animated-url]/@data-animated-url
    search_xpath = fields.CharField(255)

    # Element index, if many needed
    index = fields.IntField(null=True)

    class Meta:
        table = 'grabber'


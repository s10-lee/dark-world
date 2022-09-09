from tortoise import fields, Model
from app.db.fields import UUIDField
from app.db.utils import init_models


#
# Pinterest
#   //img[@data-animated-url]/@data-animated-url
#
# Dribble
#   //meta[@property="og:image"]/@content
#   //img[@data-test="v-img"]/@src
#
class Grabber(Model):
    id = UUIDField(pk=True)
    name = fields.CharField(255)
    icon = fields.CharField(255)
    type = fields.CharField(50, null=False, default='html')
    patterns = fields.JSONField(default=list)
    search_xpath = fields.CharField(255)
    element_index = fields.IntField(null=True)

    class Meta:
        table = 'grabber'


init_models(['app.src.grab.models'])

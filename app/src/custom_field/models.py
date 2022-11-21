from tortoise import fields, Model
from app.db.utils import init_models
from enum import Enum, IntEnum


class CustomField(Model):

    class ENTITY(IntEnum):
        case = 0
        run = 1
        defect = 2

    class TYPE(IntEnum):
        number = 0
        string = 1
        text = 2
        selectbox = 3
        checkbox = 4
        radio = 5
        multiselect = 6
        url = 7
        user = 8
        datetime = 9

    id = fields.IntField(pk=True)
    title = fields.CharField(255)
    value = fields.JSONField(null=True)
    entity = fields.IntEnumField(ENTITY, default=ENTITY.case)
    type = fields.IntEnumField(TYPE, default=TYPE.number)
    placeholder = fields.CharField(255)
    default_value = fields.CharField(255)
    is_filterable = fields.BooleanField(default=False)
    is_visible = fields.BooleanField(default=False)
    is_required = fields.BooleanField(default=False)
    is_enabled_for_all_projects = fields.BooleanField(default=False)

    class Meta:
        table = 'qs_custom_field'


init_models(['app.src.custom_field.models'])

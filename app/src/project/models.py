from tortoise import fields, Model
from app.db.utils import init_models
from app.src.user.models import User
from enum import Enum


class Project(Model):
    class ACCESS(str, Enum):
        all = 'all'
        group = 'group'
        none = 'none'

    id = fields.IntField(pk=True)
    title = fields.CharField(255)
    code = fields.CharField(16, unique=True)
    access: ACCESS = fields.CharEnumField(ACCESS, default=ACCESS.all)
    group = fields.CharField(100, null=True)
    users: fields.ReverseRelation['ProjectUsers']

    class Meta:
        table = 'qs_project'


class ProjectUsers(Model):
    class ROLE(str, Enum):
        owner = 'owner'
        admin = 'admin'
        member = 'member'

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='projects',
        on_delete=fields.CASCADE,
    )
    project: fields.ForeignKeyRelation[Project] = fields.ForeignKeyField(
        'models.Project',
        related_name='users',
        on_delete=fields.CASCADE,
    )
    role: ROLE = fields.CharEnumField(ROLE, default=ROLE.member)

    class Meta:
        table = 'qs_project_users'


init_models(['app.src.project.models'])

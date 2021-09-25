from tortoise.models import Model
from tortoise.fields import (
    IntField, UUIDField, CharField, ForeignKeyField, BooleanField, DatetimeField, ManyToManyField,
    ManyToManyRelation, ForeignKeyRelation, JSONField, TextField, ForeignKeyNullableRelation, SmallIntField,
    ReverseRelation
)
from ..user.models import User


class Job(Model):
    id = IntField(pk=True)
    name = CharField(255)
    user: ForeignKeyRelation[User] = ForeignKeyField('models.User', 'jobs')
    code = TextField(null=True)
    steps: ReverseRelation['Step']
    results: ReverseRelation['Result']

    class Meta:
        table = 'job'


class Step(Model):
    id = IntField(pk=True)
    name = CharField(255)
    code = TextField(null=True)
    data = JSONField(null=True)
    position = SmallIntField(default=0)
    job: ForeignKeyRelation[Job] = ForeignKeyField('models.Job',  related_name='steps')

    class Meta:
        table = 'job_step'
        ordering = ('job_id', 'position')


class Result(Model):
    id = IntField(pk=True)
    data = JSONField(null=True)
    created_at = DatetimeField(auto_now_add=True)
    job: ForeignKeyRelation[Job] = ForeignKeyField('models.Job',  related_name='results')

    class Meta:
        table = 'job_result'



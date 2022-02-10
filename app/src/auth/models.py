from tortoise.models import Model
from tortoise.fields import IntField, DatetimeField, TextField
from app.db.fields import UUIDField


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


class SignUpToken(Model):
    id = UUIDField(pk=True)
    created_at = DatetimeField(auto_now_add=True)
    expires_at = DatetimeField(null=True)
    activated_at = DatetimeField(null=True)

    class Meta:
        table = 'signup'

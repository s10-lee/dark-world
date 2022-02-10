from tortoise import fields
from tortoise.models import Model
from tortoise.fields import (
    ForeignKeyField as FKey,
    ForeignKeyRelation as FKeyRel,
    ForeignKeyNullableRelation as FKeyNullRel,
    BooleanField as Bool,
    CharField as Char,
    CharEnumField as Choice,
    IntField as Int,
)
from typing import Any, Optional, Union, Type
from ipaddress import IPv6Address, ip_address


class UUIDField(fields.UUIDField):
    allows_generated = True

    class _db_postgres:
        SQL_TYPE = "UUID"
        GENERATED_SQL = "UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY"

    def __init__(self, pk: bool = False, **kwargs: Any) -> None:
        if pk:
            kwargs["generated"] = bool(kwargs.get("generated", True))
        super().__init__(pk=pk, **kwargs)


class UUIDKeyUnique(fields.UUIDField):
    allows_generated = True

    class _db_postgres:
        SQL_TYPE = 'UUID'
        GENERATED_SQL = 'UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE'

    def __init__(self, **kwargs: Any) -> None:
        kwargs['unique'] = True
        kwargs['generated'] = bool(kwargs.get('generated', True))
        super().__init__(**kwargs)


class IPAddressField(fields.Field, IPv6Address):
    SQL_TYPE = "VARCHAR(39)"

    class _db_postgres:
        SQL_TYPE = "INET"

    def to_db_value(self, value: Any, instance: "Union[Type[Model], Model]") -> Optional[str]:
        return value and str(value)

    def to_python_value(self, value: Any) -> Optional[IPv6Address]:
        if isinstance(value, str):
            return ip_address(value)
        return value

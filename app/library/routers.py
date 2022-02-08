from fastapi import Depends, APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel
# from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from typing import Optional, List, Type, Any, TypeVar, Union
from app.db.models import Model, QuerySet, MODEL, QuerySetSingle
# from app.src.grab.models import User
from app.src.auth.services import get_current_auth_user


class CRUDRouter(APIRouter):
    lookup_field: str = 'pk'

    model: Union[MODEL, Any] = None
    permission = None

    schema: PydanticModel = None
    schema_in: PydanticModel = None
    schema_up: PydanticModel = None
    schema_list: PydanticListModel = None


    _http_method = {
        'list': 'GET',
        'create': 'POST',
        'update': 'PUT',
        'destroy': 'DELETE',
        'retrieve': 'GET',
    }

    def __init__(self, *args,
                 model: Any,
                 lookup_field: str = None,
                 schema: PydanticModel = None,
                 schema_in: PydanticModel = None,
                 schema_up: PydanticModel = None,
                 schema_list: PydanticListModel = None,
                 dependencies=None,
                 by_user=None,
                 **kwargs):
        super().__init__(*args, dependencies=dependencies, **kwargs)

        if model:
            self.model = model
        if lookup_field:
            self.lookup_field = lookup_field

        self.schema = schema
        self.schema_in = schema_in
        self.schema_up = schema_up or schema_in
        self.schema_list = schema_list

        self.by_user = bool(by_user)

        self._handlers = {
            'list': '/',
            'create': '/',
            'update': self.lookup_path,
            'retrieve': self.lookup_path,
            'destroy': self.lookup_path,

        }

        self._response_models = {
            # 'list': self.schema,
            'create': self.schema,
            'update': self.schema,
            'retrieve': self.schema,
            # 'destroy': None,
        }

        self._register_handlers()

    @property
    def lookup_path(self):
        return '/{pk}/'

    def _register_handlers(self):
        for name, path in self._handlers.items():
            factory = getattr(self, f'_{name}_handler')
            if not factory:
                continue
            call_handler = factory()
            http_method = self._http_method.get(name)

            self.add_api_route(
                path,
                call_handler,
                methods=[http_method],
                response_model=self._response_models.get(name),
                name=name,
            )

    def get_queryset(self, request: Request = None, **kwargs) -> QuerySet:
        if self.by_user:
            user = request.state.user
            if user:
                kwargs['user_id'] = user['id']

        return self.model.filter(**kwargs)

    def _db_lookup(self, lookup_value, request: Request = None):
        fields = {f'{self.lookup_field}': lookup_value}
        if self.by_user and request:
            fields['user_id'] = request.state.user['id']
        return fields

    def _list_handler(self):
        get_queryset = self.get_queryset
        schema_list = self.schema_list

        async def _wrapper(request: Request):
            try:
                return await schema_list.from_queryset(get_queryset(request))
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _retrieve_handler(self):
        model = self.model
        schema = self.schema
        lookup = self._db_lookup

        async def _wrapper(pk, request: Request):
            try:
                return await schema.from_tortoise_orm(await model.get(**lookup(pk, request)))
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _create_handler(self):
        model = self.model
        schema_in = self.schema_in
        by_user = self.by_user

        async def _wrapper(data: schema_in, request: Request):
            try:
                data_dict = data.dict(exclude_unset=True)
                if by_user:
                    data_dict['user_id'] = request.state.user['id']
                return await model.create(**data_dict)
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _update_handler(self):
        model = self.model
        schema = self.schema
        schema_up = self.schema_up
        lookup = self._db_lookup

        async def _wrapper(pk, data: schema_up, request: Request):
            try:
                obj = await model.get(**lookup(pk, request))
                obj.update_from_dict(data.dict(exclude_unset=True))
                await obj.save()
                return await schema.from_tortoise_orm(obj)
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _destroy_handler(self):
        model = self.model
        lookup = self._db_lookup

        async def _wrapper(pk, request: Request):
            obj = await model.filter(**lookup(pk, request)).delete()
            if not obj:
                raise HTTPException(404, 'Object does not exist')
            return obj
        return _wrapper

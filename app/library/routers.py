from fastapi import Depends, APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from datetime import datetime
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from typing import Optional, List, Type, Any, TypeVar, Union
from app.db.models import Model, QuerySet, MODEL, QuerySetSingle
from app.src.grab.models import User
from app.src.auth.services import current_auth_user


class ModelViewSet:
    lookup_field: str = 'pk'
    model: Union[MODEL, Any] = None
    schema: PydanticModel = None
    schema_in: PydanticModel = None
    schema_list: PydanticListModel = None

    def __init__(self,
                 model: Any,
                 lookup_field: str = None,
                 schema: PydanticModel = None,
                 schema_in: PydanticModel = None,
                 schema_list: PydanticListModel = None,
                 api_router: APIRouter = None,
                 **kwargs):

        if model:
            self.model = model
        if lookup_field:
            self.lookup_field = lookup_field

        if schema:
            self.schema = schema
        if schema_in:
            self.schema_in = schema_in
        if schema_list:
            self.schema_list = schema_list

        self.api_router = api_router or APIRouter(**kwargs)

        self._response_models = {
            'list': self.schema_list,
            'create': self.schema,
            'update': self.schema,
            'retrieve': self.schema,
            # 'destroy': None,
        }

    def _db_lookup(self, lookup_value):
        return {f'{self.lookup_field}': lookup_value}

    @property
    def _lookup_path(self):
        return '/{pk}/'

    def get_queryset(self, **kwargs) -> QuerySet:
        return self.model.filter(**kwargs)

    async def list(self, user: User = Depends(current_auth_user)):
        try:
            return await self.schema_list.from_queryset(self.get_queryset(user=user))
        except Exception as e:
            raise HTTPException(400, str(e))

    async def retrieve(self, pk, user: User = Depends(current_auth_user)):
        try:
            return await self.model.get(user=user, **self._db_lookup(pk))
        except Exception as e:
            raise HTTPException(400, str(e))

    async def create(self, data, user: User = Depends(current_auth_user)):
        try:
            return await self.model.create(user=user, **data.dict(exclude_unset=True))
        except Exception as e:
            raise HTTPException(400, str(e))


class CRUDRouter(APIRouter):
    lookup_field: str = 'pk'

    model: Union[MODEL, Any] = None
    permission = None

    schema: PydanticModel = None
    schema_in: PydanticModel = None
    schema_list: PydanticListModel = None
    # schema_update: BaseModel = None
    # schema_delete: BaseModel = None

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
                 schema_list: PydanticListModel = None,
                 dependencies=None,
                 **kwargs):
        super().__init__(*args, dependencies=dependencies, **kwargs)

        print('------------')
        print('dependencies :')
        print(dependencies)
        print('------------')

        if model:
            self.model = model
        if lookup_field:
            self.lookup_field = lookup_field

        if schema:
            self.schema = schema
        if schema_in:
            self.schema_in = schema_in
        if schema_list:
            self.schema_list = schema_list

        self._handlers = {
            'list': '/',
            'create': '/',
            # 'update': lookup_path,
            # 'destroy': lookup_path,
            'retrieve': self.lookup_path,
        }
        print('TYPE -----', self.schema)
        print('TYPE -----', self.schema_list)

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
            endpoint_handler = factory()
            http_method = self._http_method.get(name)
            print('-------------- ')
            print(name)
            self.add_api_route(path,
                               endpoint_handler,
                               methods=[http_method],
                               response_model=self._response_models.get(name),
                               dependencies=[Depends(current_auth_user)],
                               name=name,
                               )

    def get_queryset(self, **kwargs) -> QuerySet:
        return self.model.filter(**kwargs)

    def _db_lookup(self, lookup_value):
        return {f'{self.lookup_field}': lookup_value}

    def _list_handler(self):
        get_queryset = self.get_queryset
        schema_list = self.schema_list

        async def _wrapper(user: User = Depends(current_auth_user)):
            try:
                return await schema_list.from_queryset(get_queryset(user=user))
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _retrieve_handler(self):
        model = self.model
        lookup = self._db_lookup

        async def _wrapper(pk, user: User = Depends(current_auth_user)):
            try:
                return await model.get(user=user, **lookup(pk))
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    def _create_handler(self):
        model = self.model
        schema_in = self.schema_in

        async def _wrapper(data: schema_in, user: User = Depends(current_auth_user)):
            try:
                return await model.create(user=user, **data.dict(exclude_unset=True))
            except Exception as e:
                raise HTTPException(400, str(e))
        return _wrapper

    # async def _update_handler(self):
    #     pass
    #
    # async def _destroy_handler(self):
    #     pass

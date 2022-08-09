from fastapi import Depends, APIRouter
from app.src.scrape.models import Parser, Response
from app.src.scrape import schemas
from app.src.auth.services import get_current_user_id
from app.library.web import convert_json_to_dict, parse_html_response
from uuid import UUID

# ------------- #
#    Parser     #
# ------------- #


router = APIRouter(tags=['HTTP Parsers'])


@router.get('/ws-parser/')
async def list_parsers(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.ParserList.from_queryset(Parser.filter(user_id=user_id))


@router.post('/ws-parser/')
async def create_parser(data: schemas.ParserCreate, user_id: UUID = Depends(get_current_user_id)):
    return await Parser.create(**data.dict(), user_id=user_id)


@router.put('/ws-parser/{pk}/')
async def update_parser(pk: UUID, data: schemas.ParserCreate, user_id: UUID = Depends(get_current_user_id)):
    return await Parser.filter(id=pk, user_id=user_id).update(**data.dict())


@router.get('/ws-parser/{pk}/')
async def retrieve_parser(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await schemas.ParserReceive.from_tortoise_orm(Parser.get(id=pk, user_id=user_id))


@router.get('/ws-parser/{pk}/parse-response/{resp_id}/')
async def parse_response(pk: UUID, resp_id: int, user_id: UUID = Depends(get_current_user_id)):
    parser = await Parser.get(id=pk, user_id=user_id)
    response = await Response.get(id=resp_id)
    elements = []
    data = convert_json_to_dict(response.data)
    body = data.get('body')

    if parser.content_type == 'text/html':
        elements = parse_html_response(body, parser.search_pattern)

    return {'elements': elements, 'name': parser.name, 'search_pattern': parser.search_pattern}



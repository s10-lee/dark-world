from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from app.src.dw.models import Domain, Code
from uuid import UUID

router = APIRouter(prefix='/dw')


@router.get('/domains/')
async def get_all_domains():
    items = {}
    for domain in await Domain.all().prefetch_related('codes'):
        items[domain.url] = {
            'css': [],
            'js': []
        }
        for uid, code_type in await domain.codes.all().values_list('uid', 'code_type'):
            items[domain.url][code_type].append(uid)
    return items


@router.get('/files/{uid}/')
async def get_code(uid: UUID) -> HTMLResponse:
    try:
        code_block = await Code.get(uid=uid)
        return HTMLResponse(content=code_block.content)
    except Exception as e:
        raise HTTPException(400, str(e))


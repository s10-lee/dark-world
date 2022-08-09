from fastapi import Depends, APIRouter
from app.src.scrape.models import Variable
from app.src.scrape import schemas
from app.src.auth.services import get_current_user_id
from uuid import UUID

# --------------- #
#    Variables    #
# --------------- #


router = APIRouter(tags=['HTTP Variables'])


@router.get('/ws-variable/')
async def list_variables(user_id: UUID = Depends(get_current_user_id)):
    return await schemas.VariableList.from_queryset(Variable.filter(collection__user__id=user_id))


@router.post('/ws-variable/', response_model=schemas.VariableReceive)
async def create_variable(data: schemas.VariableCreate, user_id: UUID = Depends(get_current_user_id)):
    return await Variable.create(**data.dict())


@router.delete('/ws-variable/{pk}/')
async def destroy_variable(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await Variable.filter(id=pk, collection__user__id=user_id).delete()

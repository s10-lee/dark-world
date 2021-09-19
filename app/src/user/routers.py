from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from datetime import datetime
from uuid import UUID
from app.src.auth.models import SignUpToken
from app.src.user.models import User
from app.src.user.schemas import UserCredentials
from app.src.auth.services import (
    validate_signup,
    authentication_user,
    client_token_response,
    auth_check_refresh,
    auth_wrapper,
    get_password_hash,
)


router = APIRouter()


@router.post('/sign-up/{uid}/')
async def register_new_user(data: UserCredentials, uid: UUID = Depends(validate_signup)):
    if not (data.password and data.username):
        raise HTTPException(400, 'All fields are required')
    try:
        await User.create(username=data.username, password=get_password_hash(data.password))
        await SignUpToken.filter(id=uid).update(activated_at=datetime.utcnow())
        return {'status': 'Success', 'detail': 'User created !'}
    except Exception as e:
        print(e)

        raise HTTPException(400, 'User already exists')


@router.post('/token/obtain/')
async def auth_obtain_token(user: User = Depends(authentication_user)):
    return await client_token_response(user)


@router.post('/token/refresh/')
async def auth_refresh_token(user: User = Depends(auth_check_refresh)):
    return await client_token_response(user)


@router.get('/profile/')
async def user_profile(user: User = Depends(auth_wrapper)):
    return {'access': 'yes', 'user': user}



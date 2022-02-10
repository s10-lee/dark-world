from fastapi import Depends, APIRouter, Request
from fastapi.exceptions import HTTPException
from datetime import datetime
from uuid import UUID
from app.src.auth.models import SignUpToken
from app.src.user.models import User
from app.src.user.schemas import UserCredentials
from app.src.auth.services import (
    validate_signup,
    authenticate_user,
    client_token_response,
    auth_check_refresh,
    get_password_hash,
    get_current_auth_user,
)


router = APIRouter()


@router.post('/sign-up/{uid}/')
async def user_signup(data: UserCredentials, uid: UUID = Depends(validate_signup)):
    if not (data.password and data.email):
        raise HTTPException(400, 'All fields are required')
    try:
        await User.create(email=data.email, password=get_password_hash(data.password))
        await SignUpToken.filter(id=uid).update(activated_at=datetime.utcnow())
        return {'status': 'Success', 'detail': 'User created successfully !'}
    except Exception as e:
        print(e)
        raise HTTPException(400, 'User already exists !')


@router.post('/token/obtain/')
async def auth_obtain_token(user: User = Depends(authenticate_user)):
    return await client_token_response(user)


@router.post('/token/refresh/')
async def auth_refresh_token(user: User = Depends(auth_check_refresh)):
    return await client_token_response(user)


@router.get('/guest/')
async def user_guest(request: Request):
    return {'user': request.state.user}


@router.get('/profile/')
async def user_profile(user: User = Depends(get_current_auth_user)):
    return {'name': user.username, 'email': user.email}


@router.put('/profile/email/')
async def user_profile(request: Request, user: User = Depends(get_current_auth_user)):
    data = await request.json()
    email = data.get('email')
    if email:
        user.email = email
        await user.save()

    return {'old': user.email, 'new': email}

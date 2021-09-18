from datetime import datetime, timedelta
# from typing import Any, Union, Optional
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Security, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.src.user.models import User, RefreshToken
from app.src.user.schemas import UserCredentials
from app.src.auth.models import APIKeys, SignUpToken
from app.config.settings import JWT_SECRET, ALGORITHM, INTERVAL, APP_NAME
from uuid import UUID
import jwt
import secrets

crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
security = HTTPBearer()


def generate_private_public_keys():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048)
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.BestAvailableEncryption(bytes(JWT_SECRET, 'utf-8'))
        # crypto_serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key


async def validate_signup(uid: UUID):
    try:
        link = await SignUpToken.get(id=uid, activated_at=None)
        return link.id
    except Exception:
        raise HTTPException(status.HTTP_403_FORBIDDEN)


async def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    token = await decode_token(auth.credentials)
    return token


async def auth_check_refresh(refresh_token: str = Cookie(None)):
    try:
        token = await RefreshToken.get(token=refresh_token, expires_at__gte=datetime.utcnow())
        await token.fetch_related('user')
        await token.user.fetch_related('perms')
        return await token.user
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Refresh token not found or expired')


async def decode_token(token):
    item = await APIKeys.first()

    try:
        payload = jwt.decode(token, item.public_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Signature has expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


async def authentication_user(data: UserCredentials):
    user = await User.get_or_none(username=data.username, is_active=True)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    elif not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Inactive user')
    await user.fetch_related('perms')
    await user.logged()
    return user


async def create_access_token(user: User) -> str:
    item = await APIKeys.first()

    private_key = crypto_serialization.load_pem_private_key(
        bytes(item.private_key, 'utf-8'),
        bytes(JWT_SECRET, 'utf-8'),
        crypto_default_backend()
    )

    headers = {
        'kid': str(item.id),
    }
    payload = {
        'iss': APP_NAME,
        'exp': datetime.utcnow() + timedelta(days=0, minutes=INTERVAL),
        'iat': datetime.utcnow(),
        'sub': str(user.id),
        'name': user.username,
        'perms': [perm.slug for perm in user.perms]
    }

    return jwt.encode(payload, private_key, algorithm=ALGORITHM, headers=headers)


async def create_refresh_token(user: User) -> RefreshToken:
    return await RefreshToken.create(
        user=user,
        token=secrets.token_urlsafe(48),
        expires_at=datetime.utcnow() + timedelta(days=10)
    )


async def client_token_response(user: User) -> JSONResponse:
    refresh_token = await create_refresh_token(user)
    access_token = await create_access_token(user)
    response = JSONResponse(content={
        'access_token': access_token,
    })
    seconds = refresh_token.expires()
    response.set_cookie(
        key='refresh_token',
        value=refresh_token.token,
        expires=seconds,
        path='/',
        httponly=True,
    )
    return response


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return crypt.hash(password)




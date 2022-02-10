from tortoise.contrib.pydantic import pydantic_model_creator
from app.src.user.models import User


UserCredentials = pydantic_model_creator(
    User,
    name='UserCredentials',
    include=('email', 'password')
)



# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
import pytest
# import asyncio
# from typing import Generator
from httpx import AsyncClient
# from fastapi.testclient import TestClient
# from tortoise.contrib.test import finalizer, initializer
# from app.src.user.models import User
from app.main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": "Tomato"}


# @pytest.fixture(scope="module")
# def client() -> Generator:
#     initializer(["models"])
#     with TestClient(app) as c:
#         yield c
#     finalizer()
#
#
# @pytest.fixture(scope="module")
# def event_loop(client: TestClient) -> Generator:
#     yield client.task.get_loop()  # type: ignore
#
#
# def test_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
#     response = client.post("/users", json={"username": "admin"})
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["username"] == "admin"
#     assert "id" in data
#     user_id = data["id"]
#
#     async def get_user_by_db():
#         user = await User.get(id=user_id)
#         return user
#
#     user_obj = event_loop.run_until_complete(get_user_by_db())
#     assert user_obj.id == user_id

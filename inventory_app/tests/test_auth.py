from datetime import timedelta

import pytest

from fastapi import HTTPException
from inventory_app.main import app
from inventory_app.routers.auth import (
    ALGORITH, SECRET_KEY, authenticate_user, create_access_token, get_current_user, get_db)
from inventory_app.tests.conftest import TestingSessionLocal, override_get_db
from jose import jwt

app.dependency_overrides[get_db] = override_get_db
db = TestingSessionLocal()


def test_authenticate_user(test_user):
    authenticated_user = authenticate_user(test_user["username"], "test123", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user["username"]


def test_authenticate_nonexistent_user(test_user):
    authenticated_user = authenticate_user("wrongusername", "test123", db)
    assert authenticated_user is False


def test_authenticate_nonexistent_password(test_user):
    authenticated_user = authenticate_user(test_user["username"], "wrongpassword", db)
    assert authenticated_user is False


def test_create_access_token():
    username = "bob"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = \
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH], options={"verify_signature": False})
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "bob", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITH)

    user = await get_current_user(token)
    assert user == {"username": "bob", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITH)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user"

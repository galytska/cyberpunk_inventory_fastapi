from fastapi.testclient import TestClient
from inventory_app.routers.users import get_current_user, get_db

users_get_current_user = get_current_user
users_get_db = get_db


def test_return_user(client: TestClient, test_user):
    response = client.get("/user/")
    assert response.status_code == 200
    test_user["id"] = 1
    assert response.json() == test_user

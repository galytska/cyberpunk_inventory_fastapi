from fastapi.testclient import TestClient
from inventory_app.routers.admin import get_current_user, get_db
from inventory_app.tests.conftest import get_db_item_by_id
from inventory_app.tests.utils import generate_random_number

admin_get_current_user = get_current_user
admin_get_db = get_db


def test_admin_read_all_authenticated(client: TestClient, test_item: dict):
    response = client.get("/admin/items")
    test_item["id"] = 1
    assert response.status_code == 200
    assert response.json() == [test_item]


def test_delete_item(client: TestClient, test_item: dict):
    response = client.delete("/admin/items/1")
    assert response.status_code == 204
    assert get_db_item_by_id(item_id=1) is None


def test_delete_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    response = client.delete(f"/admin/items/{nonexistent_item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

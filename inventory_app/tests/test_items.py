from fastapi.testclient import TestClient
from inventory_app.models import Item
from inventory_app.tests.conftest import TestingSessionLocal, expected_item, get_db_item_by_id
from inventory_app.tests.utils import generate_random_number, update_item


def test_read_items_smoke(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_items(client: TestClient, test_item: dict):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [expected_item]


def test_read_item_by_id(client: TestClient, test_item: dict):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == expected_item


def test_read_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    response = client.get(f"/items/{nonexistent_item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item(client: TestClient, tear_down_clear_items_table):
    request_data = {
        "name": "phone",
        "description": "mobile phone",
        "category": "gadget",
        "quantity": 5,
        "price": 100.5,
        "owner_id": 1
    }
    response = client.post(
        "/items/",
        json=request_data,
    )
    assert response.status_code == 200

    data = response.json()
    item_id = data["id"]
    db = TestingSessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    assert db_item.name == request_data["name"]
    assert db_item.description == request_data["description"]
    assert db_item.category == request_data["category"]
    assert db_item.quantity == request_data["quantity"]
    assert db_item.price == request_data["price"]


def test_create_existing_item(client: TestClient, test_item: dict):
    response = client.post(
        "/items/",
        json=test_item,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item with such name already registered"}


def test_delete_item(client: TestClient, test_item: dict):
    response = client.delete(f"/items/1")
    assert response.status_code == 204
    assert get_db_item_by_id(item_id=1) is None


def test_delete_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    response = client.delete(f"/items/{nonexistent_item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item(client: TestClient, test_item):
    test_item_gadget_updated = update_item(test_item)
    response = client.put("/items/1", json=test_item_gadget_updated)
    assert response.status_code == 204

    db_item = get_db_item_by_id(1)
    assert db_item.name == test_item_gadget_updated["name"]
    assert db_item.description == test_item_gadget_updated["description"]
    assert db_item.category == test_item_gadget_updated["category"]
    assert db_item.quantity == test_item_gadget_updated["quantity"]
    assert db_item.price == test_item_gadget_updated["price"]


def test_update_nonexistent_item_id(client: TestClient, test_item):
    nonexistent_item_id = generate_random_number()
    response = client.put(f"/items/{nonexistent_item_id}", json=test_item)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

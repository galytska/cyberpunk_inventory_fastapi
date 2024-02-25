import random

from pytest import mark

from fastapi.testclient import TestClient


@mark.smoke
def test_read_main(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@mark.smoke
def test_create_item(client: TestClient):
    response = client.post(
        "/items/",
        json={
            "name": "phone",
            "description": "mobile phone",
            "category": "gadget",
            "quantity": 5,
            "price": 100.5
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "phone"
    assert "id" in data
    item_id = data["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "phone"
    assert data["id"] == item_id


def test_read_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    response = client.get(f"/items/{nonexistent_item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_existing_item(client: TestClient):
    test_item_weapon = {
        "name": "water gun",
        "description": "no harm",
        "category": "weapon",
        "quantity": 5,
        "price": 100.5
    }
    response = client.post(
        "/items/",
        json=test_item_weapon,
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/items/",
        json=test_item_weapon,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item with such name already registered"}


def test_delete_item(client: TestClient):
    response = client.post(
        "/items/",
        json={
            "name": "arm",
            "description": "cyber arm",
            "category": "cybernetic",
            "quantity": 3,
            "price": 1000.5
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    response = client.delete(f"/items/{nonexistent_item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item(client: TestClient):
    test_item_gadget = {
        "name": "night vision device",
        "description": "night vision",
        "category": "gadget",
        "quantity": 9,
        "price": 90.9
    }
    response = client.post(
        "/items/",
        json=test_item_gadget,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    test_item_gadget_updated = update_item(test_item_gadget)
    response = client.put(f"/items/{item_id}", json=test_item_gadget_updated)
    assert response.status_code == 204

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    data.pop('id')
    assert data == test_item_gadget_updated


def test_update_nonexistent_item_id(client: TestClient):
    nonexistent_item_id = generate_random_number()
    test_item_gadget = {
        "name": "night vision device",
        "description": "night vision",
        "category": "gadget",
        "quantity": 9,
        "price": 90.9
    }

    response = client.put(f"/items/{nonexistent_item_id}", json=test_item_gadget)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def generate_random_number():
    """
    generate random 6 digits number e.g. 123456
    """
    return random.randint(100000, 999999)


def update_item(item: dict) -> dict:
    return {k: v + ' updated' if isinstance(v, str) else v + 1
            for k, v in item.items()
            }

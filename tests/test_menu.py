from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_menu_item():
    response = client.post("/menu/", json={
        "name": "Burger",
        "price": 9.99,
        "is_available": True
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Burger"

def test_get_available_items():
    response = client.get("/menu/available/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

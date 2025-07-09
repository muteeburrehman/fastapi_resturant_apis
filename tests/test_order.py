from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_place_order():
    menu_resp = client.post("/menu/", json={
        "name": "Soda",
        "price": 1.99,
        "is_available": True
    })
    menu_id = menu_resp.json()["id"]

    order_resp = client.post("/order/", json={
        "customer_name": "Alice",
        "item_ids": [menu_id]
    })
    assert order_resp.status_code == 200
    assert order_resp.json()["customer_name"] == "Alice"
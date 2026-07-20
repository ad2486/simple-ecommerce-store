def test_list_products_returns_empty_list(client):
    resp = client.get("/products")
    assert resp.status_code == 200
    assert resp.json == []


def test_create_product(client):
    resp = client.post("/products", json={
        "name": "Mouse",
        "price": 50.0,
        "stock": 10
    })
    assert resp.status_code == 201
    assert resp.json["name"] == "Mouse"
    assert resp.json["price"] == "50.00"
    assert resp.json["stock"] == 10


def test_create_product_returns_id(client):
    resp = client.post("/products", json={
        "name": "Teclado",
        "price": 100.0,
        "stock": 5
    })
    assert resp.status_code == 201
    assert isinstance(resp.json["id"], int)
    assert resp.json["id"] == 1


def test_list_products_after_create(client):
    client.post("/products", json={"name": "Mouse", "price": 50.0, "stock": 10})
    client.post("/products", json={"name": "Teclado", "price": 100.0, "stock": 5})

    resp = client.get("/products")
    assert resp.status_code == 200
    assert len(resp.json) == 2


def test_get_product_by_id(client):
    create_resp = client.post("/products", json={
        "name": "Monitor", "price": 800.0, "stock": 3
    })
    product_id = create_resp.json["id"]

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json["name"] == "Monitor"
    assert resp.json["price"] == "800.00"


def test_get_product_not_found(client):
    resp = client.get("/products/999")
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


def test_update_product(client):
    create_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = create_resp.json["id"]

    resp = client.put(f"/products/{product_id}", json={
        "name": "Mouse Gamer", "price": 150.0, "stock": 7
    })
    assert resp.status_code == 200
    assert resp.json["name"] == "Mouse Gamer"
    assert resp.json["price"] == "150.00"
    assert resp.json["stock"] == 7


def test_update_product_not_found(client):
    resp = client.put("/products/999", json={
        "name": "Nada", "price": 0, "stock": 0
    })
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


def test_delete_product(client):
    create_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = create_resp.json["id"]

    resp = client.delete(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json["message"] == "Product deleted"


def test_delete_product_not_found(client):
    resp = client.delete("/products/999")
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


def test_delete_actually_removes_product(client):
    create_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = create_resp.json["id"]

    client.delete(f"/products/{product_id}")

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 404

# Verifica se a listagem de pedidos retorna uma lista vazia
# quando ainda não foi criado nenhum pedido
def test_list_orders_returns_empty_list(client):
    resp = client.get("/orders")
    assert resp.status_code == 200
    assert resp.json == []


# Cria um usuário e um produto, depois cria um pedido com 1 item
# Verifica status 201, public_code e total_amount
def test_create_order_success(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    product_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = product_resp.json["id"]

    resp = client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": product_id, "quantity": 2}]
    })
    assert resp.status_code == 201
    assert resp.json["public_code"].startswith("ORD-")
    assert resp.json["total_amount"] == "100.00"
    assert resp.json["status"] == "pending"


# Cria um pedido e verifica que o estoque do produto foi reduzido
def test_create_order_reduces_stock(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    product_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = product_resp.json["id"]

    client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": product_id, "quantity": 3}]
    })

    resp = client.get(f"/products/{product_id}")
    assert resp.json["stock"] == 7


# Cria um pedido e depois verifica que ele aparece na listagem
def test_list_orders_after_create(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    product_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = product_resp.json["id"]

    client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": product_id, "quantity": 1}]
    })

    resp = client.get("/orders")
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]["total_amount"] == "50.00"


# Tenta criar pedido com user_id que não existe → 404
def test_create_order_user_not_found(client):
    resp = client.post("/orders", json={
        "user_id": 999,
        "items": [{"product_id": 1, "quantity": 1}]
    })
    assert resp.status_code == 404
    assert resp.json["error"] == "User not found"


# Tenta criar pedido com product_id que não existe → 404
def test_create_order_product_not_found(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    resp = client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": 999, "quantity": 1}]
    })
    assert resp.status_code == 404
    assert resp.json["error"] == "Product 999 not found"


# Tenta comprar mais do que o estoque disponível → 400
def test_create_order_insufficient_stock(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    product_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 2
    })
    product_id = product_resp.json["id"]

    resp = client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": product_id, "quantity": 5}]
    })
    assert resp.status_code == 400
    assert resp.json["error"] == f"Insufficient stock for product {product_id}"


# Cria um pedido e verifica que os OrderItems foram gerados
def test_create_order_creates_order_items(client):
    user_resp = client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    user_id = user_resp.json["id"]

    p1 = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    }).json
    p2 = client.post("/products", json={
        "name": "Teclado", "price": 100.0, "stock": 5
    }).json

    client.post("/orders", json={
        "user_id": user_id,
        "items": [
            {"product_id": p1["id"], "quantity": 2},
            {"product_id": p2["id"], "quantity": 1}
        ]
    })

    resp = client.get("/test-order-items")
    assert resp.status_code == 200
    assert len(resp.json) == 2

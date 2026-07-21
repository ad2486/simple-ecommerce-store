# Verifica se a listagem de produtos retorna uma lista vazia
# quando ainda não foi cadastrado nenhum produto
def test_list_products_returns_empty_list(client):
    resp = client.get("/products")
    assert resp.status_code == 200
    assert resp.json == []


# Cria um produto via POST e verifica se os dados retornados
# conferem com o que foi enviado (inclusive price vindo como string)
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


# Confirma que o produto criado ganha um ID inteiro (auto-increment)
# e que o primeiro produto tem id = 1
def test_create_product_returns_id(client):
    resp = client.post("/products", json={
        "name": "Teclado",
        "price": 100.0,
        "stock": 5
    })
    assert resp.status_code == 201
    assert isinstance(resp.json["id"], int)
    assert resp.json["id"] == 1


# Cria dois produtos e depois verifica se a listagem retorna os dois
# Garante que o GET lista corretamente após inserções
def test_list_products_after_create(client):
    client.post("/products", json={"name": "Mouse", "price": 50.0, "stock": 10})
    client.post("/products", json={"name": "Teclado", "price": 100.0, "stock": 5})

    resp = client.get("/products")
    assert resp.status_code == 200
    assert len(resp.json) == 2


# Cria um produto e depois busca ele pelo ID específico
# Verifica que os dados do produto retornado estão corretos
def test_get_product_by_id(client):
    create_resp = client.post("/products", json={
        "name": "Monitor", "price": 800.0, "stock": 3
    })
    product_id = create_resp.json["id"]

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json["name"] == "Monitor"
    assert resp.json["price"] == "800.00"


# Tenta buscar um produto com ID inexistente e espera erro 404
# com a mensagem "Product not found"
def test_get_product_not_found(client):
    resp = client.get("/products/999")
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


# Cria um produto, depois altera nome/preço/estoque via PUT
# Verifica que os novos valores foram salvos e retornados
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


# Tenta atualizar um produto que não existe e espera 404
def test_update_product_not_found(client):
    resp = client.put("/products/999", json={
        "name": "Nada", "price": 0, "stock": 0
    })
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


# Cria um produto e depois deleta ele
# Verifica que a resposta é 200 com a mensagem de confirmação
def test_delete_product(client):
    create_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = create_resp.json["id"]

    resp = client.delete(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json["message"] == "Product deleted"


# Tenta deletar um produto que não existe e espera 404
def test_delete_product_not_found(client):
    resp = client.delete("/products/999")
    assert resp.status_code == 404
    assert resp.json["error"] == "Product not found"


# Garante que depois de deletar o produto, ele realmente some do banco:
# buscar por ele retorna 404
def test_delete_actually_removes_product(client):
    create_resp = client.post("/products", json={
        "name": "Mouse", "price": 50.0, "stock": 10
    })
    product_id = create_resp.json["id"]

    client.delete(f"/products/{product_id}")

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 404

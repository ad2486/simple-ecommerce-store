# Verifica se a listagem de usuários retorna uma lista vazia
# quando ainda não foi cadastrado nenhum usuário
def test_list_users_returns_empty_list(client):
    resp = client.get("/users")
    assert resp.status_code == 200
    assert resp.json == []


# Cria um usuário via POST e verifica se os dados retornados
# conferem com o que foi enviado (senha NÃO volta na resposta)
def test_create_user(client):
    resp = client.post("/users", json={
        "name": "Ana Silva",
        "email": "ana@example.com",
        "password": "123456"
    })
    assert resp.status_code == 201
    assert resp.json["name"] == "Ana Silva"
    assert resp.json["email"] == "ana@example.com"
    assert "id" in resp.json
    assert "password" not in resp.json


# Tenta cadastrar dois usuários com o mesmo e-mail
# O segundo deve ser rejeitado com status 409 (Conflict)
def test_create_user_duplicate_email(client):
    client.post("/users", json={
        "name": "Ana",
        "email": "ana@example.com",
        "password": "123"
    })

    resp = client.post("/users", json={
        "name": "Outra Ana",
        "email": "ana@example.com",
        "password": "456"
    })
    assert resp.status_code == 409
    assert resp.json["error"] == "Email already registered"


# Cria um usuário e verifica se ele aparece na listagem
def test_list_users_after_create(client):
    client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })
    client.post("/users", json={
        "name": "Bruno", "email": "bruno@example.com", "password": "456"
    })

    resp = client.get("/users")
    assert resp.status_code == 200
    assert len(resp.json) == 2
    assert resp.json[0]["name"] == "Ana"
    assert resp.json[1]["name"] == "Bruno"


# Verifica que a senha nunca é retornada em nenhum usuário da listagem
def test_list_users_does_not_expose_password(client):
    client.post("/users", json={
        "name": "Ana", "email": "ana@example.com", "password": "123"
    })

    resp = client.get("/users")
    assert resp.status_code == 200
    for user in resp.json:
        assert "password" not in user
        assert "password_hash" not in user

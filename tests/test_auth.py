# Cria um usuário e faz login com email/senha corretos
# Verifica que retorna 200 com os dados do usuário (sem a senha)
def test_login_success(client):
    client.post("/users", json={
        "name": "Ana",
        "email": "ana@example.com",
        "password": "123456"
    })

    resp = client.post("/login", json={
        "email": "ana@example.com",
        "password": "123456"
    })
    assert resp.status_code == 200
    assert resp.json["name"] == "Ana"
    assert resp.json["email"] == "ana@example.com"
    assert "password" not in resp.json


# Tenta logar com um e-mail que não existe no banco
# Deve retornar 404
def test_login_email_not_found(client):
    resp = client.post("/login", json={
        "email": "naoexiste@example.com",
        "password": "123"
    })
    assert resp.status_code == 404
    assert resp.json["error"] == "User not found"


# Tenta logar com e-mail existente mas senha errada
# Deve retornar 401
def test_login_wrong_password(client):
    client.post("/users", json={
        "name": "Ana",
        "email": "ana@example.com",
        "password": "123456"
    })

    resp = client.post("/login", json={
        "email": "ana@example.com",
        "password": "senha_errada"
    })
    assert resp.status_code == 401
    assert resp.json["error"] == "Invalid password"

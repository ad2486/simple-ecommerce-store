# Testes automatizados — Simple E-commerce Store

## Objetivo

Adicionar testes automatizados com `pytest` para garantir que a API funciona
e continua funcionando depois de futuras alterações.

## Tecnologias

- **pytest** — framework de testes
- **SQLite em memória** — banco separado para não sujar o banco real

## O que testar (prioridade)

### 1. Rotas de produto (GET, POST, PUT, DELETE)
- GET /products retorna 200 e lista
- GET /products/<id> retorna 200 e produto correto
- GET /products/<id> retorna 404 se não existir
- POST /products cria e retorna 201
- PUT /products/<id> atualiza e retorna 200
- PUT /products/<id> retorna 404 se não existir
- DELETE /products/<id> retorna 200
- DELETE /products/<id> retorna 404 se já deletado

### 2. Rotas de usuário (GET, POST)
- GET /users retorna 200 e lista
- POST /users cria e retorna 201
- POST /users com email duplicado retorna 409

### 3. Login
- POST /login com dados corretos retorna 200
- POST /login com senha errada retorna 401
- POST /login com email inexistente retorna 404

### 4. Pedidos (GET, POST)
- POST /orders com dados válidos retorna 201
- POST /orders com usuário inválido retorna 404
- POST /orders com produto inexistente retorna 404
- POST /orders com estoque insuficiente retorna 400

## Estrutura sugerida

```
simple-ecommerce-store/
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # configuração do Flask e banco de teste
│   ├── test_products.py
│   ├── test_users.py
│   ├── test_auth.py
│   └── test_orders.py
```

### conftest.py

O `conftest.py` fornece um "app de teste" e um "cliente de teste" para os
testes usarem. O banco é recriado a cada teste (isolamento total).

```python
import pytest
from app import create_app, db as database

@pytest.fixture
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        database.create_all()
        yield app
        database.session.rollback()
        database.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

### Estrutura de um teste

```python
def test_list_products(client):
    resp = client.get("/products")
    assert resp.status_code == 200
    assert isinstance(resp.json, list)
```

## Como rodar

```bash
.venv/bin/python -m pytest tests/ -v
```

O `-v` mostra o nome de cada teste e se passou ou falhou.

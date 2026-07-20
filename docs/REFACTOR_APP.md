# Refatoração: migrar de `main.py` único para `app/`

## Objetivo

Separar o `main.py` atual (~270 linhas) em módulos organizados dentro de uma
pasta `app/`, mantendo tudo funcionando sem quebrar as rotas existentes.

## Estrutura final

```
simple-ecommerce-store/
├── main.py              # só 3 linhas: cria o app e roda
├── app/
│   ├── __init__.py      # configura Flask, SQLAlchemy, importa rotas
│   ├── models.py        # User, Product, Order, OrderItem
│   └── routes/
│       ├── __init__.py
│       ├── products.py  # GET /products, POST /products
│       ├── users.py     # GET /users, POST /users
│       └── orders.py    # GET /orders, POST /orders, GET /test-order-items
```

## Passo a passo

### 1. Criar `app/__init__.py`

Mover daqui do `main.py`:
- Importações: Flask, SQLAlchemy, datetime
- Criação do `app = Flask(__name__)`
- Config `SQLALCHEMY_DATABASE_URI`
- Criação do `db = SQLAlchemy()` e `db.init_app(app)`
- Import dos modelos (`from app import models`) para garantir que as classes
  sejam registradas no SQLAlchemy
- Import das rotas (`from app.routes import products, users, orders`)
- Exportar `app` e `db`

### 2. Criar `app/models.py`

Mover as 4 classes (User, Product, Order, OrderItem) **exatamente como estão**.
Importar `db` de `app` (vai dar um import circular, resolver com import
adiado — importar dentro da função ou usar `db` do pacote).

Na prática: em `app/models.py`:
```python
from app import db
from datetime import datetime
```

### 3. Criar `app/routes/__init__.py`

Vazio ou só um comentário.

### 4. Criar `app/routes/products.py`

Mover:
- Importações necessárias (Flask `request`, `db`, `Product`)
- Rota `GET /products` → decorator `@app_routes.get(...)` ou usar Blueprint
- Rota `POST /products`

### 5. Criar `app/routes/users.py`

Mover:
- `GET /users`, `POST /users`

### 6. Criar `app/routes/orders.py`

Mover:
- `GET /orders`, `POST /orders`, `GET /test-order-items`

### 7. Simplificar `main.py`

```python
from app import app

if __name__ == "__main__":
    app.run(debug=True)
```

## Como evitar import circular

O problema clássico: `app/__init__.py` cria o `db`, mas `app/models.py`
precisa do `db`, e `app/routes/*.py` precisam do `db` e dos modelos.

Solução: usar **Blueprint** em vez de decorators diretos no `app`, ou então:

Em `app/__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
    db.init_app(app)

    from app import models
    from app.routes import products, users, orders

    return app
```

E em `main.py`:
```python
from app import create_app

app = create_app()
```

Os models importam `db` de `app` e funciona porque o `db` é criado antes dos
models serem importados.

## Ordem sugerida

1. Criar `app/__init__.py` com `create_app()` e `db`
2. Criar `app/models.py` com os 4 modelos (testar se o Flask sobe)
3. Criar `app/routes/` e mover as rotas uma por uma, testando cada vez
4. No fim, reduzir `main.py`

## Teste após cada passo

- Rodar `python main.py` e ver se sobe sem erro
- Testar cada GET e POST no Postman

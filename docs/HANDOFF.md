# Handoff — Simple E-commerce Store

## Objetivo do projeto

Projeto de aprendizado: uma API simples de e-commerce para praticar Python, Flask, SQL, SQLite e SQLAlchemy. O foco é entender a lógica, não receber soluções prontas.

Leia também `docs/PLAN.md` antes de sugerir mudanças.

## Como ajudar o usuário

- Responder em português, de forma curta e direta.
- Explicar sintaxe e motivo das decisões antes de avançar.
- O usuário escreve o código. Dê requisitos, pequenos trechos e revisão; só entregue código completo quando ele pedir explicitamente.
- Ao definir uma tabela, modelo ou função, informar todas as regras relevantes de uma vez (`NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, chaves estrangeiras). Não deixar requisitos implícitos.
- Não inventar complexidade: sem autenticação, Docker, migrations, React ou arquitetura avançada por enquanto.
- Se houver erro, explicar a causa e a menor correção possível.

## Estado atual

### Ambiente e Git

- Ambiente virtual `.venv` criado pelo PyCharm.
- Repositório Git criado.
- `.gitignore` ignora `.venv/`, `instance/`, `*.db`, `.idea/`, `.env` e arquivos temporários.
- `instance/ecommerce.db` existe localmente e não deve ir para o Git.
- `requirements.txt` contém `Flask` e `Flask-SQLAlchemy`.

### Estrutura do projeto

O código foi refatorado de `main.py` único para pacote `app/`:

```
simple-ecommerce-store/
├── main.py              # só 2 linhas: from app import create_app; app = create_app()
├── app/
│   ├── __init__.py      # create_app(), db, registra Blueprints
│   ├── models.py        # User, Product, Order, OrderItem
│   └── routes/
│       ├── general.py   # GET /, GET /health
│       ├── products.py  # GET /products, POST /products
│       ├── users.py     # GET /users, POST /users
│       └── orders.py    # GET /orders, POST /orders, GET /test-order-items
```

- A URI é `sqlite:///ecommerce.db` (aponta para `instance/ecommerce.db`).
- O objeto `db` é criado com `SQLAlchemy()` e ligado ao Flask com `db.init_app(app)` dentro de `create_app()`.
- As rotas abaixo funcionam e foram testadas no Postman:
  - `GET /` retorna uma mensagem de que a API está rodando
  - `GET /health` retorna `{"status": "ok"}`
  - `GET /users` lista todos os usuários
  - `GET /products` lista todos os produtos
  - `GET /orders` lista todos os pedidos
  - `GET /test-order-items` lista todos os itens de pedidos (rota temporária de teste)
  - `POST /products` cadastra um novo produto
  - `POST /users` cadastra um novo usuário (com hash de senha via `werkzeug.security`)
  - `POST /orders` cria um pedido com itens, valida estoque, calcula total e atualiza estoque

Cada arquivo de rota usa `Blueprint` em vez de decorator direto no `app`. Os Blueprints são registrados em `app/__init__.py`.

Observação: iniciar o Flask sem erro valida a configuração básica. A conexão foi confirmada consultando o banco via modelos SQLAlchemy.

### Banco SQLite criado manualmente

O usuário criou e conferiu as quatro tabelas diretamente no terminal `sqlite3`, dentro de `instance/ecommerce.db`.

#### `users`

- `id INTEGER PRIMARY KEY`
- `name TEXT NOT NULL`
- `email TEXT NOT NULL UNIQUE`
- `password_hash TEXT NOT NULL`
- `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`

Foi inserido um usuário de teste:

```text
Ana Silva | ana@example.com | hash_falso_apenas_para_aprender
```

O `UNIQUE` de e-mail foi testado: uma segunda inserção com o mesmo e-mail foi recusada.

#### `products`

- `id INTEGER PRIMARY KEY`
- `name TEXT NOT NULL`
- `description TEXT` (opcional)
- `price NUMERIC NOT NULL CHECK(price >= 0)`
- `stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)`
- `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`

#### `orders`

- `id INTEGER PRIMARY KEY`
- `public_code TEXT NOT NULL UNIQUE`
- `user_id INTEGER NOT NULL REFERENCES users(id)`
- `status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'paid', 'cancelled'))`
- `total_amount NUMERIC NOT NULL DEFAULT 0 CHECK(total_amount >= 0)`
- `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`

#### `order_items`

- `id INTEGER PRIMARY KEY`
- `order_id INTEGER NOT NULL REFERENCES orders(id)`
- `product_id INTEGER NOT NULL REFERENCES products(id)`
- `quantity INTEGER NOT NULL CHECK(quantity > 0)`
- `unit_price NUMERIC NOT NULL CHECK(unit_price >= 0)`
- `UNIQUE(order_id, product_id)`

O usuário executou `PRAGMA foreign_keys = ON;` no terminal SQLite e verificou as tabelas. Importante: essa configuração vale apenas para a conexão atual; quando necessário, habilitar chaves estrangeiras também nas conexões abertas pelo Flask/SQLAlchemy.

### Modelos SQLAlchemy em `app/models.py`

As quatro classes (User, Product, Order, OrderItem) foram movidas para
`app/models.py`, mapeando exatamente as tabelas existentes.

Não foi chamado `db.create_all()` em momento algum. O banco permanece
compatível com os modelos. Alterações futuras de esquema exigirão migrations
ou alteração manual no SQLite.

## Próximo passo recomendado

Agora que as rotas POST estão prontas, os próximos passos sugeridos (qualquer ordem):

1. **Login** (`POST /login`) — validar senha com `check_password_hash`
2. **CRUD de produtos** — `GET /products/<id>`, `PUT /products/<id>`, `DELETE /products/<id>`
3. **Frontend HTML/CSS/JS** consumindo a API

O `main.py` já foi simplificado para apenas `from app import create_app; app = create_app()`. Toda a lógica está em `app/`.

## Etapas concluídas

- [x] Modelos SQLAlchemy e consultas básicas (GET em todas as tabelas)
- [x] Testes com Postman
- [x] `POST /products` — cadastro de produtos
- [x] `POST /users` — cadastro de usuários com hash de senha
- [x] `POST /orders` — criação de pedidos com itens, validação de estoque, cálculo de total e atualização de estoque

## Próximas etapas maiores

1. [x] Cadastro de produtos pela API (POST /products)
2. [x] Cadastro de usuários com hash de senha (POST /users)
3. [x] Criação de pedidos, itens, cálculo de total e atualização de estoque (POST /orders)
4. [ ] Login e sessão (POST /login, check_password_hash)
5. [ ] CRUD completo de produtos (GET /<id>, PUT, DELETE)
6. [ ] Frontend HTML/CSS/JavaScript (depois da API estável)

## Situação do Git

Foram feitos 5 commits até o momento:

```
5179fd5 feat: add POST routes for products, users and orders
b06c3b0 feat: add User model and GET /users route
f578c9a feat: add Product model and GET /products route
3ce066c feat: add Order model and GET /orders route
94a5b32 add OrderItem model and GET /test-order-items route for future testing
```

Tudo commitado. O banco em `instance/` continua ignorado pelo Git.

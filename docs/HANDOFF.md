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

### Flask

`main.py` já cria o Flask e configura o SQLAlchemy:

- A aplicação usa `Flask(__name__)`.
- A URI é `sqlite:///ecommerce.db`.
  - No Flask-SQLAlchemy, esse caminho relativo aponta para a pasta `instance/`, portanto ele acessa `instance/ecommerce.db`.
- O objeto `db` é criado com `SQLAlchemy()` e ligado ao Flask com `db.init_app(app)`.
- As rotas abaixo funcionam e foram testadas no Postman:
  - `GET /` retorna uma mensagem de que a API está rodando
  - `GET /health` retorna `{"status": "ok"}`
  - `GET /users` lista todos os usuários
  - `GET /products` lista todos os produtos
  - `GET /orders` lista todos os pedidos
  - `GET /test-order-items` lista todos os itens de pedidos (rota temporária de teste)

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

### Modelos SQLAlchemy criados no `main.py`

Os quatro modelos foram criados, mapeando exatamente as tabelas existentes. Nenhuma alteração foi feita no banco — os modelos apenas lêem as tabelas criadas manualmente.

Modelos criados na seguinte ordem:

1. **`User`** (`__tablename__ = "users"`) — colunas: id, name, email (unique), password_hash, created_at
2. **`Product`** (`__tablename__ = "products"`) — colunas: id, name, description, price (Numeric), stock, created_at; CHECKs: price >= 0, stock >= 0
3. **`Order`** (`__tablename__ = "orders"`) — colunas: id, public_code (unique), user_id (FK → users.id), status (default "pending"), total_amount (default 0), created_at; CHECKs: status IN ('pending','paid','cancelled'), total_amount >= 0
4. **`OrderItem`** (`__tablename__ = "order_items"`) — colunas: id, order_id (FK → orders.id), product_id (FK → products.id), quantity, unit_price; CHECKs: quantity > 0, unit_price >= 0; UniqueConstraint(order_id, product_id)

Todos os modelos foram testados via GET no Postman (retornam lista vazia ou os dados existentes).

Não foi chamado `db.create_all()` em momento algum. O banco permanece compatível com os modelos. Alterações futuras de esquema exigirão migrations ou alteração manual no SQLite.

## Próximo passo recomendado

Criar rotas `POST` para cadastrar dados via API. Sugestão de ordem:

1. **`POST /products`** — mais simples, sem dependências de outras tabelas
2. **`POST /users`** — introduz hash de senha (usar `werkzeug.security`)
3. **`POST /orders`** — criar pedido com itens, calcular total, validar e atualizar estoque (o mais complexo, envolve transação)

Manter toda a lógica no `main.py` por enquanto; refatorar para `app/` somente quando o arquivo começar a crescer.

## Etapas concluídas

- [x] Modelos SQLAlchemy e consultas básicas (GET em todas as tabelas)
- [x] Testes com Postman

## Próximas etapas maiores

1. [ ] Cadastro e listagem de produtos pela API (POST /products)
2. [ ] Cadastro de usuários e login básico (POST /users, hash de senha)
3. [ ] Criação de pedidos, itens, cálculo de total e atualização de estoque
4. [ ] Frontend HTML/CSS/JavaScript (depois da API estável)

## Situação do Git

Foram feitos 4 commits nesta sessão:

```
b06c3b0 feat: add User model and GET /users route
f578c9a feat: add Product model and GET /products route
3ce066c feat: add Order model and GET /orders route
94a5b32 add OrderItem model and GET /test-order-items route for future testing
```

Tudo commitado. O banco em `instance/` continua ignorado pelo Git.

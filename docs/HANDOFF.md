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
- As rotas abaixo funcionam e foram testadas no navegador:
  - `GET /` retorna uma mensagem de que a API está rodando.
  - `GET /health` retorna `{"status": "ok"}`.

Observação: iniciar o Flask sem erro valida a configuração básica, mas a conexão real será confirmada ao consultar o banco via um modelo SQLAlchemy.

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

## Próximo passo recomendado

Criar o primeiro modelo SQLAlchemy, `User`, e consultar a tabela existente pela API.

Para não aumentar a complexidade agora:

1. Manter o primeiro modelo no `main.py`; os arquivos vazios em `app/` podem ser usados numa refatoração posterior.
2. Explicar que uma classe que herda de `db.Model` representa uma tabela.
3. Definir explicitamente `__tablename__ = "users"`, pois a tabela já existe e se chama `users`.
4. Fazer as colunas do modelo corresponderem exatamente às colunas e regras acima.
5. Criar uma rota temporária ou definitiva para listar usuários e confirmar que SQLAlchemy lê o banco.
6. Só então criar os modelos `Product`, `Order` e `OrderItem`, um por vez, explicando as relações.

Não chamar `db.create_all()` nesta fase. Ele não atualiza tabelas existentes se o modelo mudar; futuramente, alterações de esquema exigirão migrations. O banco foi criado manualmente para aprender SQL e deve continuar compatível com os modelos.

## Próximas etapas maiores

1. Modelos SQLAlchemy e consultas básicas.
2. Cadastro e listagem de produtos pela API.
3. Cadastro de usuários e login básico.
4. Criação de pedidos, itens, cálculo de total e atualização de estoque.
5. Testes com Postman, Insomnia ou Thunder Client.
6. Frontend HTML/CSS/JavaScript somente depois que a API básica estiver estável.

## Situação do Git

Antes de continuar, conferir `git status`. No momento deste handoff, `main.py` e `requirements.txt` tinham alterações ainda não commitadas. O banco em `instance/` deve permanecer ignorado.

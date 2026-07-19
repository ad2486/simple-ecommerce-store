# Planejamento — E-commerce simples com Flask e SQL

## Objetivo

Criar uma loja simples de periféricos de computador para praticar SQL, Flask e relações entre tabelas sem adicionar muitas tecnologias de uma vez.

Exemplos de produtos: mouse, teclado, monitor, headset, SSD e memória RAM.

## Tecnologias

- **Backend:** Python + Flask
- **Banco de dados:** SQLite no início ou PostgreSQL depois
- **Acesso ao banco:** SQLAlchemy
- **Frontend:** HTML, CSS e JavaScript puro (opcional na primeira etapa)
- **Testes da API:** Postman, Insomnia ou Thunder Client
- **Versionamento:** Git e GitHub

## Visão geral

```text
Frontend (HTML/CSS/JS ou ferramenta de API)
                |
             HTTP/JSON
                |
          Backend Flask
                |
           SQLAlchemy
                |
      SQLite ou PostgreSQL
```

No começo, a API pode ser testada diretamente por uma ferramenta como Postman. O frontend entra quando o backend básico estiver funcionando.

## Banco de dados — primeira versão

### `users`

Guarda os usuários da loja.

- `id` — chave primária sequencial
- `name`
- `email` — único
- `password_hash` — senha nunca deve ser salva em texto puro
- `created_at`

### `products`

Guarda os produtos disponíveis.

- `id` — chave primária sequencial
- `name`
- `description`
- `price`
- `stock`
- `created_at`

### `orders`

Guarda cada pedido feito por um usuário.

- `id` — chave primária interna sequencial
- `public_code` — código público aleatório e único, por exemplo `ORD-9A4K82F1`
- `user_id` — chave estrangeira para `users`
- `status` — por enquanto, `pending`, `paid`, `cancelled`
- `total_amount`
- `created_at`

### `order_items`

Guarda os itens de cada pedido.

- `id` — chave primária sequencial
- `order_id` — chave estrangeira para `orders`
- `product_id` — chave estrangeira para `products`
- `quantity`
- `unit_price` — preço do produto no momento da compra

## Relacionamentos

```text
Usuário 1 ─── N Pedidos
Pedido  1 ─── N Itens do pedido
Produto 1 ─── N Itens do pedido
```

Um pedido tem vários produtos e um produto pode aparecer em vários pedidos. A tabela `order_items` resolve essa relação.

## Funcionalidades da primeira versão

### Usuários

- Cadastrar usuário
- Fazer login
- Listar ou consultar perfil básico

### Produtos

- Cadastrar produto
- Listar produtos
- Consultar produto por ID
- Editar produto
- Excluir produto

### Pedidos

- Criar pedido para um usuário
- Adicionar produtos e quantidades
- Calcular o total
- Salvar o preço de cada item no momento da compra
- Listar pedidos de um usuário
- Ver detalhes de um pedido

## Regras importantes

- Validar se existe estoque antes de criar o pedido.
- Não aceitar quantidade menor ou igual a zero.
- Não permitir e-mail repetido.
- Não salvar senhas puras; salvar apenas o hash.
- Usar transação ao criar um pedido: ou tudo é salvo e o estoque é atualizado, ou nada muda.
- Expor `public_code` ao cliente, não o ID interno sequencial do pedido.

## Estrutura inicial do backend

```text
simple-ecommerce-store/
│
├── main.py                 # ponto de entrada: inicia o Flask
├── requirements.txt        # bibliotecas do projeto
├── .gitignore              # arquivos que o Git não deve enviar
├── README.md               # como instalar e executar o projeto
│
├── docs/
│   └── PLAN.md             # este planejamento
│
└── app/                    # código da aplicação (criar depois)
    ├── __init__.py         # cria e configura a aplicação Flask
    ├── models.py           # modelos/tabelas do banco de dados
    │
    ├── routes/             # endpoints da API
    │   ├── users.py        # rotas de usuários
    │   ├── products.py     # rotas de produtos
    │   └── orders.py       # rotas de pedidos
    │
    └── services/           # regras de negócio mais complexas
        └── orders.py       # criação de pedido e controle de estoque
```

No início, bastam `main.py` e `app/models.py`. Crie `routes/` quando houver endpoints e `services/` somente quando a lógica de pedidos começar a ficar grande.

## Ordem sugerida de implementação

1. Criar o repositório Git e configurar o ambiente Python/Flask.
2. Criar o banco SQLite e as quatro tabelas com SQLAlchemy.
3. Implementar cadastro e listagem de produtos.
4. Implementar cadastro de usuários e login básico.
5. Criar pedidos e itens de pedido.
6. Validar estoque, calcular total e diminuir estoque ao finalizar o pedido.
7. Testar todos os endpoints em uma ferramenta de API.
8. Criar um frontend simples com HTML, CSS e JavaScript consumindo a API.
9. Migrar de SQLite para PostgreSQL quando a versão básica estiver estável.

## Expansões futuras

- Categorias de produtos
- Carrinho de compras
- Endereços
- Imagens de produtos
- Pagamento simulado
- Status mais completos: enviado e entregue
- Painel administrativo
- Busca, filtros e paginação
- Avaliações e favoritos
- Testes automatizados
- Docker e deploy

## Consultas SQL para praticar depois

- Produtos mais vendidos
- Clientes que mais compraram
- Faturamento por mês
- Produtos sem estoque
- Ticket médio dos pedidos

## Limite da primeira entrega

A primeira versão está pronta quando for possível cadastrar usuários e produtos, criar pedidos com vários itens, validar estoque e consultar os pedidos pela API. O frontend pode vir depois.

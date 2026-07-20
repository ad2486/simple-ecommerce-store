from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from secrets import token_hex

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
db = SQLAlchemy()
db.init_app(app)

# Tables

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("price >= 0"),
        db.CheckConstraint("stock >= 0")
    )

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    public_code = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="pending")
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("status IN ('pending', 'paid', 'cancelled')"),
        db.CheckConstraint("total_amount >= 0")
    )

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        db.CheckConstraint("quantity > 0"),
        db.CheckConstraint("unit_price >= 0"),
        db.UniqueConstraint("order_id", "product_id")
    )

# Routes

## GET routes

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users")
def users():
    users_list = User.query.all()
    return [
        {
         "id":u.id,
         "name":u.name,
         "email":u.email
         }
        for u in users_list
    ]

@app.get("/products")
def products():
    products_list = Product.query.all()
    return [
        {
         "id":p.id,
         "name":p.name,
         "description":p.description,
         "price": str(p.price),
         "stock": p.stock,
         "created_at": p.created_at.isoformat()
        }
        for p in products_list
    ]

@app.get("/orders")
def orders():
    orders_list = Order.query.all()
    return [
        {
         "id":o.id,
         "public_code":o.public_code,
         "user_id":o.user_id,
         "status":o.status,
         "total_amount":str(o.total_amount),
         "created_at":o.created_at.isoformat()
        }
        for o in orders_list
    ]

@app.get("/test-order-items")
def order_items():
    order_items_list = OrderItem.query.all()
    return [
        {
         "id":to.id,
         "order_id":to.order_id,
         "product_id":to.product_id,
         "quantity":to.quantity,
         "unit_price":str(to.unit_price)
        }
        for to in order_items_list
    ]

## POST routes

@app.post("/products")
def create_product():
    data = request.get_json()

    # 1 - Extrair os campos do JSON
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock", 0)

    # 2 - Criar o objeto Product
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock
    )

    # 3 - Salvar no banco
    db.session.add(product)
    db.session.commit()

    # 4 - Retornar o produto criado com status 201
    return {
        "id": product.id,
        "description": product.description,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock
    }, 201

@app.post("/users")
def create_user():
    data = request.get_json()

    # 1 - Extrair os campos do JSON
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # 2 - Verificar se possui um usuário com o mesmo email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already registered"}, 409

    # 3 - Gerar o hash da senha
    p_hash = generate_password_hash(password)

    # 4 - Criar o objeto User
    user = User(
        name=name,
        email=email,
        password_hash=p_hash
    )

    # 5 - Salvar no banco
    db.session.add(user)
    db.session.commit()

    # 6 - Retornar o usuário criado com status 201
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }, 201

@app.post("/orders")
def create_order():
    data = request.get_json()

    # 1 - Extrair os campos do JSON
    user_id = data.get("user_id")
    items = data.get("items")

    # 2 - Gerar código público único
    while True:
        public_code = "ORD-" + token_hex(4).upper()
        if not Order.query.filter_by(public_code=public_code).first():
            break

    # 3 - Validar se o usuário existe
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # 4 - Loop dos items
    total_amount = 0
    order_items = []
    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")
        product = Product.query.get(product_id)
        if not product:
            return {"error": f"Product {product_id} not found"}, 404
        if product.stock < quantity:
            return {"error": f"Insufficient stock for product {product_id}"}, 400
        unit_price = product.price
        total_amount += quantity * unit_price
        order_items.append({
            "product": product,
            "quantity": quantity,
            "unit_price": unit_price
        })
        product.stock -= quantity

    # 5 - Criar o objeto Order
    order = Order(
        public_code=public_code,
        user_id=user_id,
        total_amount=total_amount,
    )
    db.session.add(order)

    # 6 - Criar os objetos OrderItems
    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["produc"].id,
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.session.add(order_item)

    # 7 - Commit geral e retorno
    db.session.commit()
    return {
        "public_code": order.public_code,
        "total_amount": str(order.total_amount),
        "status": order.status,
    }, 201


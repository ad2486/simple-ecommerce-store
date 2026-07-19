from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

# Routes

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




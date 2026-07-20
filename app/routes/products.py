from flask import Blueprint, request
from app import db
from app.models import Product

products_bp = Blueprint("products", __name__)


@products_bp.get("/products")
def list_products():
    products_list = Product.query.all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": str(p.price),
            "stock": p.stock,
            "created_at": p.created_at.isoformat()
        }
        for p in products_list
    ]


@products_bp.post("/products")
def create_product():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock", 0)

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock
    )

    db.session.add(product)
    db.session.commit()

    return {
        "id": product.id,
        "description": product.description,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock
    }, 201

from flask import Blueprint, request
from secrets import token_hex
from app import db
from app.models import Order, OrderItem, Product, User

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/orders")
def list_orders():
    orders_list = Order.query.all()
    return [
        {
            "id": o.id,
            "public_code": o.public_code,
            "user_id": o.user_id,
            "status": o.status,
            "total_amount": str(o.total_amount),
            "created_at": o.created_at.isoformat()
        }
        for o in orders_list
    ]


@orders_bp.post("/orders")
def create_order():
    data = request.get_json()

    user_id = data.get("user_id")
    items = data.get("items")

    while True:
        public_code = "ORD-" + token_hex(4).upper()
        if not Order.query.filter_by(public_code=public_code).first():
            break

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

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

    order = Order(
        public_code=public_code,
        user_id=user_id,
        total_amount=total_amount,
    )
    db.session.add(order)
    db.session.flush()

    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.session.add(order_item)

    db.session.commit()
    return {
        "public_code": order.public_code,
        "total_amount": str(order.total_amount),
        "status": order.status,
    }, 201


@orders_bp.get("/test-order-items")
def test_order_items():
    order_items_list = OrderItem.query.all()
    return [
        {
            "id": to.id,
            "order_id": to.order_id,
            "product_id": to.product_id,
            "quantity": to.quantity,
            "unit_price": str(to.unit_price)
        }
        for to in order_items_list
    ]

from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

users_bp = Blueprint("users", __name__)


@users_bp.get("/users")
def list_users():
    users_list = User.query.all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email
        }
        for u in users_list
    ]


@users_bp.post("/users")
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already registered"}, 409

    p_hash = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        password_hash=p_hash
    )

    db.session.add(user)
    db.session.commit()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }, 201

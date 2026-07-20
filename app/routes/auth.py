from flask import Blueprint, request
from app import db
from app.models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404

    if check_password_hash(user.password_hash, password):
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }, 200
    else:
        return {"error": "Invalid password"}, 401
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"

    db.init_app(app)

    from app import models
    from app.routes.general import general_bp
    from app.routes.products import products_bp
    from app.routes.users import users_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(general_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)

    return app

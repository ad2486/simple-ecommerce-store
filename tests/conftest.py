import pytest
from app import create_app, db as database

@pytest.fixture
def app():
    app = create_app(test_config={
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })

    with app.app_context():
        database.create_all()
        yield app
        database.session.rollback()
        database.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
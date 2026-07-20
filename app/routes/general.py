from flask import Blueprint

general_bp = Blueprint("general", __name__)


@general_bp.get("/")
def home():
    return {"message": "API is running"}


@general_bp.get("/health")
def health():
    return {"status": "ok"}

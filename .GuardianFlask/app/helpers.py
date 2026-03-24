from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(hashed: str, password: str) -> bool:
    return check_password_hash(hashed, password)


def generate_reset_token(email: str) -> str:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="password-reset-salt")


def verify_reset_token(token: str):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    max_age = current_app.config.get("TOKEN_EXPIRATION_SECONDS", 1800)
    try:
        return s.loads(token, salt="password-reset-salt", max_age=max_age)
    except Exception:
        return None
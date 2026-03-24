import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Flask ---
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # --- Base de Datos ---
    DB_USER     = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Puchys2005")
    DB_HOST     = os.getenv("DB_HOST", "localhost")
    DB_PORT     = os.getenv("DB_PORT", "3306")
    DB_NAME     = os.getenv("DB_NAME", "guardian_zero2")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Mail (Gmail SMTP) ---
    MAIL_SERVER         = "smtp.gmail.com"
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USERNAME       = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD       = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    # --- Token de recuperación (expira en 30 min) ---
    TOKEN_EXPIRATION_SECONDS = 1800
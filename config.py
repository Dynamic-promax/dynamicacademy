"""
Application configuration.

Reads settings from environment variables (see .env.example). Values here
are sensible local-development defaults - copy .env.example to .env and
change SECRET_KEY / ADMIN_EMAIL / ADMIN_PASSWORD before deploying.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # --- Core Flask settings -------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-in-production")

    # --- Database --------------------------------------------------------------
    # SQLite for local development. To use PostgreSQL in production, set
    # DATABASE_URL to something like:
    #   postgresql://username:password@localhost:5432/dynamic_academy
    # SQLAlchemy works with either connection string with no code changes.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dynamic_academy.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- File uploads ------------------------------------------------------
    # Uploaded tutor CVs/certificates are stored OUTSIDE the public static
    # folder so they can never be accessed by guessing a URL - only admins
    # (via a login-protected route) can download them.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads", "tutors")
    ALLOWED_UPLOAD_EXTENSIONS = {"pdf", "doc", "docx"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB max upload size

    # --- Admin bootstrap ---------------------------------------------------
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@dynamicacademy.ng")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeThisPassword123!")

    # --- Sessions ------------------------------------------------------------
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # --- Academy info (also mirrored in app/utils/academy.py for templates) -
    ACADEMY_PHONE = "09090575783"
    ACADEMY_WHATSAPP = "2348119001010"  # registration/contact WhatsApp number
    ACADEMY_ADDRESS = "Apex Garden Estate, Kukwaba District, Abuja, Nigeria"
    
    SESSION_COOKIE_SECURE = True
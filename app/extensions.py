"""
Central place where Flask extension objects live.

They are created here (unbound) and then attached to the app inside
app/__init__.py's create_app() factory. This avoids circular imports:
any module can `from app.extensions import db` without importing the
whole app package.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access the admin dashboard."
login_manager.login_message_category = "warning"

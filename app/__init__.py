"""
Application factory.

`create_app()` builds and configures the Flask app: loads config,
attaches extensions (db, csrf, login), registers blueprints (route
groups), and registers a couple of CLI commands used during setup
(`flask init-db`, `flask create-admin`, `flask seed-courses`).
"""
import os
from flask import Flask, render_template

from config import Config
from app.extensions import db, csrf, login_manager


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Make sure the instance folder (holds the SQLite DB + uploads) exists.
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --- Extensions ----------------------------------------------------
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    # --- Blueprints ------------------------------------------------------
    from app.routes.main import main_bp
    from app.routes.courses import courses_bp
    from app.routes.programs import programs_bp
    from app.routes.registration import registration_bp
    from app.routes.tutor import tutor_bp
    from app.routes.contact import contact_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(tutor_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # --- Template context: academy info available on every page ----------
    from app.utils.academy import ACADEMY, WHATSAPP_MESSAGES
    from app.utils.helpers import whatsapp_link

    @app.context_processor
    def inject_academy_info():
        from datetime import datetime
        return {
            "academy": ACADEMY,
            "whatsapp_messages": WHATSAPP_MESSAGES,
            "whatsapp_link": whatsapp_link,
            "current_year": datetime.utcnow().year,
        }

    # --- Error pages -------------------------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template("413.html"), 413

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    # --- CLI commands (see README for usage) --------------------------------
    register_cli_commands(app)

    return app


def register_cli_commands(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db():
        """Create all database tables. Usage: flask init-db"""
        with app.app_context():
            db.create_all()
        print("Database tables created.")

    @app.cli.command("create-admin")
    def create_admin():
        """
        Create (or update) the admin account using ADMIN_EMAIL /
        ADMIN_PASSWORD from the environment (see .env). Usage: flask create-admin
        """
        from app.models import AdminUser

        with app.app_context():
            email = app.config["ADMIN_EMAIL"]
            password = app.config["ADMIN_PASSWORD"]
            admin = AdminUser.query.filter_by(email=email).first()
            if admin:
                admin.set_password(password)
                db.session.commit()
                print(f"Existing admin '{email}' password updated.")
            else:
                admin = AdminUser(name="Dynamic Academy Admin", email=email)
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                print(f"Admin account created: {email}")

    @app.cli.command("seed-courses")
    def seed_courses():
        """Populate the course catalogue with the full Dynamic Academy offering. Usage: flask seed-courses"""
        from app.seed_data import seed_all

        with app.app_context():
            seed_all()
        print("Courses, programmes and demo blog posts seeded.")

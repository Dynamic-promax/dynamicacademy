"""Admin authentication: login and logout."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.forms import AdminLoginForm
from app.models import AdminUser

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = AdminUser.query.filter_by(email=form.email.data.strip().lower()).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Welcome back, {admin.name}.", "success")
            return redirect(next_page or url_for("admin.dashboard"))
        flash("Invalid email or password.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/admin/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

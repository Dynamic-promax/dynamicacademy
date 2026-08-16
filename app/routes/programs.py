"""Public 'Upcoming Programs' listing and detail pages."""
from flask import Blueprint, render_template, abort

from app.models import Program

programs_bp = Blueprint("programs", __name__)


@programs_bp.route("/programs")
def program_list():
    all_programs = Program.query.filter_by(is_published=True).order_by(Program.created_at.desc()).all()
    return render_template("programs.html", programs=all_programs)


@programs_bp.route("/programs/<slug>")
def program_detail(slug):
    program = Program.query.filter_by(slug=slug, is_published=True).first()
    if not program:
        abort(404)
    return render_template("program_detail.html", program=program)
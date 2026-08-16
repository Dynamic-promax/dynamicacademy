"""
Course catalogue: listing (with category filter), course detail, and the
"Enroll Now" chooser that asks "Are you a Student or Parent/Guardian?"
before handing off to the right registration form with the course
pre-selected.
"""
from flask import Blueprint, render_template, request, abort

from app.models import Course

courses_bp = Blueprint("courses", __name__)

CATEGORIES = [
    ("technology", "Technology & Digital Skills"),
    ("academic", "Academic Support"),
    ("exam-prep", "Examination Preparation"),
    ("languages", "Languages"),
]


@courses_bp.route("/courses")
def course_list():
    category = request.args.get("category", "all")
    query = Course.query.filter_by(is_published=True)
    if category != "all":
        query = query.filter_by(category=category)
    courses = query.order_by(Course.title).all()
    return render_template("courses.html", courses=courses, categories=CATEGORIES, active_category=category)


@courses_bp.route("/courses/<slug>")
def course_detail(slug):
    course = Course.query.filter_by(slug=slug, is_published=True).first()
    if not course:
        abort(404)
    related = Course.query.filter(
        Course.category == course.category, Course.slug != slug, Course.is_published == True
    ).limit(3).all()
    return render_template("course_detail.html", course=course, related=related)


@courses_bp.route("/enroll/<slug>")
def enroll_choice(slug):
    """
    'Enroll Now' on a course page lands here: choose Student or
    Parent/Guardian, then continue to the matching registration form
    with ?course=<slug> so it's pre-selected automatically.
    """
    course = Course.query.filter_by(slug=slug, is_published=True).first()
    if not course:
        abort(404)
    return render_template("enroll_choice.html", course=course)

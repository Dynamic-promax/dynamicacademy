"""
Student and Parent/Guardian registration.

Both routes:
  1. Pre-populate the course dropdown from the database.
  2. Pre-select a course if ?course=<slug> was passed (e.g. from the
     "Enroll Now" flow on a course page).
  3. Validate with WTForms (CSRF included automatically).
  4. Save a real row to the database.
  5. Generate a unique registration number (DA-STU-2026-0001 / DA-PAR-...).
  6. Show a real success page with that registration number.
"""
from flask import Blueprint, render_template, redirect, url_for, request

from app.extensions import db
from app.forms import StudentRegistrationForm, ParentRegistrationForm
from app.models import Course, Student, ParentGuardian, Child, Enrollment
from app.utils.helpers import generate_registration_number

registration_bp = Blueprint("registration", __name__)


def _course_choices():
    """(value, label) pairs for course <select> fields, built fresh from the DB."""
    courses = Course.query.filter_by(is_published=True).order_by(Course.title).all()
    choices = [("", "Select a course")] + [(c.slug, c.title) for c in courses]
    return choices


@registration_bp.route("/student-register", methods=["GET", "POST"])
def student_register():
    form = StudentRegistrationForm()
    form.course.choices = _course_choices()

    preselected_slug = request.args.get("course", "")
    if request.method == "GET" and preselected_slug:
        form.course.data = preselected_slug

    if form.validate_on_submit():
        course = Course.query.filter_by(slug=form.course.data).first()

        count_so_far = Student.query.count()
        reg_number = generate_registration_number("STU", count_so_far)

        student = Student(
            registration_number=reg_number,
            full_name=form.full_name.data.strip(),
            date_of_birth=form.date_of_birth.data,
            age=form.age.data,
            gender=form.gender.data,
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            address=form.address.data,
            course_id=course.id if course else None,
            course_name_snapshot=course.title if course else form.course.data,
            learning_mode=form.learning_mode.data,
            preferred_schedule=form.preferred_schedule.data,
            experience_level=form.experience_level.data,
            current_school=form.current_school.data,
            referral_source=form.referral_source.data,
            additional_info=form.additional_info.data,
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.flush()  # get student.id before commit

        db.session.add(Enrollment(course_id=course.id if course else None, student_id=student.id))
        db.session.commit()

        return redirect(url_for("registration.success", kind="student", ref=reg_number))

    return render_template("student_register.html", form=form)


@registration_bp.route("/parent-register", methods=["GET", "POST"])
def parent_register():
    form = ParentRegistrationForm()
    form.course.choices = _course_choices()

    preselected_slug = request.args.get("course", "")
    if request.method == "GET" and preselected_slug:
        form.course.data = preselected_slug

    if form.validate_on_submit():
        course = Course.query.filter_by(slug=form.course.data).first()

        parent = ParentGuardian(
            full_name=form.parent_full_name.data.strip(),
            email=form.parent_email.data.strip().lower(),
            phone=form.parent_phone.data.strip(),
            whatsapp_number=form.parent_whatsapp.data,
            relationship_to_child=form.relationship_to_child.data,
            address=form.parent_address.data,
            emergency_contact_name=form.emergency_contact_name.data,
            emergency_contact_phone=form.emergency_contact_phone.data,
            emergency_contact_relationship=form.emergency_contact_relationship.data,
        )
        db.session.add(parent)
        db.session.flush()  # get parent.id

        count_so_far = Child.query.count()
        reg_number = generate_registration_number("PAR", count_so_far)

        child = Child(
            registration_number=reg_number,
            parent_id=parent.id,
            full_name=form.child_full_name.data.strip(),
            date_of_birth=form.child_date_of_birth.data,
            age=form.child_age.data,
            gender=form.child_gender.data,
            current_school=form.child_school.data,
            grade_class=form.child_grade.data,
            course_id=course.id if course else None,
            course_name_snapshot=course.title if course else form.course.data,
            learning_mode=form.learning_mode.data,
            preferred_schedule=form.preferred_schedule.data,
            experience_level=form.experience_level.data,
            learning_goals=form.learning_goals.data,
            additional_info=form.additional_info.data,
        )
        db.session.add(child)
        db.session.flush()

        db.session.add(Enrollment(course_id=course.id if course else None, child_id=child.id))
        db.session.commit()

        return redirect(url_for("registration.success", kind="parent", ref=reg_number))

    return render_template("parent_register.html", form=form)


@registration_bp.route("/registration-success")
def success():
    kind = request.args.get("kind", "student")
    ref = request.args.get("ref", "")
    return render_template("registration_success.html", kind=kind, ref=ref)

"""
Admin dashboard: everything here requires login (@login_required).

Sections:
  - Dashboard overview (counts)
  - Students / Parents & Children / Tutor Applications (list + detail + status update)
  - Courses (list + add + edit + delete)
  - Contact messages / Newsletter subscribers
  - Secure tutor CV/certificate download
"""
import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    send_from_directory, abort, current_app
)
from flask_login import login_required

from app.extensions import db
from app.models import (
    Student, ParentGuardian, Child, TutorApplication, Course, Program,
    ContactMessage, NewsletterSubscriber, RegistrationStatus
)
from app.forms import CourseForm, ProgramForm, StatusUpdateForm

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "total_students": Student.query.count(),
        "total_parents": ParentGuardian.query.count(),
        "total_children": Child.query.count(),
        "total_tutors": TutorApplication.query.count(),
        "total_courses": Course.query.count(),
        "total_messages": ContactMessage.query.count(),
        "pending_students": Student.query.filter_by(status=RegistrationStatus.PENDING).count(),
        "pending_children": Child.query.filter_by(status=RegistrationStatus.PENDING).count(),
        "pending_tutors": TutorApplication.query.filter_by(status=RegistrationStatus.PENDING).count(),
    }
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    recent_children = Child.query.order_by(Child.created_at.desc()).limit(5).all()
    recent_tutors = TutorApplication.query.order_by(TutorApplication.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html", stats=stats,
        recent_students=recent_students, recent_children=recent_children,
        recent_tutors=recent_tutors, recent_messages=recent_messages,
    )


# ---------------------------------------------------------------------------
# STUDENTS
# ---------------------------------------------------------------------------
@admin_bp.route("/students")
@login_required
def students():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")
    query = Student.query
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(Student.full_name.ilike(like), Student.email.ilike(like), Student.registration_number.ilike(like)))
    if status_filter:
        query = query.filter_by(status=status_filter)
    records = query.order_by(Student.created_at.desc()).all()
    return render_template("admin/students.html", students=records, search=search,
                            status_filter=status_filter, statuses=RegistrationStatus.CHOICES)


@admin_bp.route("/students/<int:student_id>", methods=["GET", "POST"])
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    form = StatusUpdateForm(status=student.status)
    if form.validate_on_submit():
        student.status = form.status.data
        db.session.commit()
        flash(f"Status updated to '{student.status}'.", "success")
        return redirect(url_for("admin.student_detail", student_id=student.id))
    return render_template("admin/student_detail.html", student=student, form=form)


# ---------------------------------------------------------------------------
# PARENTS & CHILDREN
# ---------------------------------------------------------------------------
@admin_bp.route("/parents")
@login_required
def parents():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")
    query = Child.query.join(ParentGuardian)
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(
            Child.full_name.ilike(like), Child.registration_number.ilike(like),
            ParentGuardian.full_name.ilike(like), ParentGuardian.email.ilike(like),
        ))
    if status_filter:
        query = query.filter(Child.status == status_filter)
    records = query.order_by(Child.created_at.desc()).all()
    return render_template("admin/parents.html", children=records, search=search,
                            status_filter=status_filter, statuses=RegistrationStatus.CHOICES)


@admin_bp.route("/parents/<int:child_id>", methods=["GET", "POST"])
@login_required
def parent_detail(child_id):
    child = Child.query.get_or_404(child_id)
    form = StatusUpdateForm(status=child.status)
    if form.validate_on_submit():
        child.status = form.status.data
        db.session.commit()
        flash(f"Status updated to '{child.status}'.", "success")
        return redirect(url_for("admin.parent_detail", child_id=child.id))
    whatsapp_note = (
        f"Hello {child.parent.full_name}, this is Dynamic Academy regarding "
        f"{child.full_name}'s registration {child.registration_number}."
    )
    return render_template(
        "admin/parent_detail.html", child=child, parent=child.parent, form=form, whatsapp_note=whatsapp_note
    )

# ---------------------------------------------------------------------------
# TUTOR APPLICATIONS
# ---------------------------------------------------------------------------
@admin_bp.route("/tutors")
@login_required
def tutor_applications():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")
    query = TutorApplication.query
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(
            TutorApplication.full_name.ilike(like), TutorApplication.email.ilike(like),
            TutorApplication.application_number.ilike(like),
        ))
    if status_filter:
        query = query.filter_by(status=status_filter)
    records = query.order_by(TutorApplication.created_at.desc()).all()
    return render_template("admin/tutors.html", applications=records, search=search,
                            status_filter=status_filter, statuses=RegistrationStatus.CHOICES)


@admin_bp.route("/tutors/<int:application_id>", methods=["GET", "POST"])
@login_required
def tutor_detail(application_id):
    application = TutorApplication.query.get_or_404(application_id)
    form = StatusUpdateForm(status=application.status)
    if form.validate_on_submit():
        application.status = form.status.data
        db.session.commit()
        flash(f"Status updated to '{application.status}'.", "success")
        return redirect(url_for("admin.tutor_detail", application_id=application.id))
    return render_template("admin/tutor_detail.html", application=application, form=form)


@admin_bp.route("/tutors/<int:application_id>/download/<doc_type>")
@login_required
def download_tutor_document(application_id, doc_type):
    """
    Securely serve a tutor's CV or certificate. Only reachable by a
    logged-in admin (@login_required) - the files themselves live
    outside /static so they are never publicly guessable.
    """
    application = TutorApplication.query.get_or_404(application_id)
    filename = application.cv_filename if doc_type == "cv" else application.certificate_filename
    subfolder = "cv" if doc_type == "cv" else "certificates"
    if not filename:
        abort(404)
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    return send_from_directory(folder, filename, as_attachment=True)


# ---------------------------------------------------------------------------
# COURSES (add / edit / delete)
# ---------------------------------------------------------------------------
def _slugify(title: str) -> str:
    import re
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


@admin_bp.route("/courses")
@login_required
def courses():
    all_courses = Course.query.order_by(Course.category, Course.title).all()
    return render_template("admin/courses.html", courses=all_courses)


@admin_bp.route("/courses/new", methods=["GET", "POST"])
@login_required
def course_new():
    form = CourseForm()
    if form.validate_on_submit():
        slug = _slugify(form.title.data)
        if Course.query.filter_by(slug=slug).first():
            flash("A course with a very similar title already exists. Please choose a different title.", "error")
        else:
            course = Course(slug=slug)
            form.populate_obj(course)
            db.session.add(course)
            db.session.commit()
            flash(f"Course '{course.title}' created.", "success")
            return redirect(url_for("admin.courses"))
    return render_template("admin/course_form.html", form=form, course=None)


@admin_bp.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def course_edit(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.commit()
        flash(f"Course '{course.title}' updated.", "success")
        return redirect(url_for("admin.courses"))
    return render_template("admin/course_form.html", form=form, course=course)


@admin_bp.route("/courses/<int:course_id>/delete", methods=["POST"])
@login_required
def course_delete(course_id):
    course = Course.query.get_or_404(course_id)
    title = course.title
    db.session.delete(course)
    db.session.commit()
    flash(f"Course '{title}' deleted.", "info")
    return redirect(url_for("admin.courses"))

# ---------------------------------------------------------------------------
# PROGRAMS (Upcoming Programs — bootcamps, corporate training, etc.)
# ---------------------------------------------------------------------------
@admin_bp.route("/programs")
@login_required
def programs():
    all_programs = Program.query.order_by(Program.created_at.desc()).all()
    return render_template("admin/programs.html", programs=all_programs)


@admin_bp.route("/programs/new", methods=["GET", "POST"])
@login_required
def program_new():
    form = ProgramForm()
    if form.validate_on_submit():
        slug = _slugify(form.title.data)
        if Program.query.filter_by(slug=slug).first():
            flash("A programme with a very similar title already exists. Please choose a different title.", "error")
        else:
            program = Program(slug=slug)
            form.populate_obj(program)
            db.session.add(program)
            db.session.commit()
            flash(f"Programme '{program.title}' created.", "success")
            return redirect(url_for("admin.programs"))
    return render_template("admin/program_form.html", form=form, program=None)


@admin_bp.route("/programs/<int:program_id>/edit", methods=["GET", "POST"])
@login_required
def program_edit(program_id):
    program = Program.query.get_or_404(program_id)
    form = ProgramForm(obj=program)
    if form.validate_on_submit():
        form.populate_obj(program)
        db.session.commit()
        flash(f"Programme '{program.title}' updated.", "success")
        return redirect(url_for("admin.programs"))
    return render_template("admin/program_form.html", form=form, program=program)


@admin_bp.route("/programs/<int:program_id>/delete", methods=["POST"])
@login_required
def program_delete(program_id):
    program = Program.query.get_or_404(program_id)
    title = program.title
    db.session.delete(program)
    db.session.commit()
    flash(f"Programme '{title}' deleted.", "info")
    return redirect(url_for("admin.programs"))

# ---------------------------------------------------------------------------
# CONTACT MESSAGES & NEWSLETTER
# ---------------------------------------------------------------------------
@admin_bp.route("/messages")
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=all_messages)


@admin_bp.route("/messages/<int:message_id>/resolve", methods=["POST"])
@login_required
def resolve_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_resolved = not message.is_resolved
    db.session.commit()
    return redirect(url_for("admin.messages"))


@admin_bp.route("/newsletter")
@login_required
def newsletter():
    subscribers = NewsletterSubscriber.query.order_by(NewsletterSubscriber.subscribed_at.desc()).all()
    return render_template("admin/newsletter.html", subscribers=subscribers)

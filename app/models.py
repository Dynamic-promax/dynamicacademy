"""
Database models (Flask-SQLAlchemy).

Each class here becomes a table. Relationships are defined with
db.relationship() so, for example, `student.course` gives you the
related Course object directly.

To add a new field to a table:
  1. Add the column below.
  2. Delete instance/dynamic_academy.db (local dev only!) and run
     `flask init-db` again - OR use a migration tool (Flask-Migrate)
     for production so you don't lose existing data.
"""
from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


# ---------------------------------------------------------------------------
# ADMIN USER
# ---------------------------------------------------------------------------
class AdminUser(UserMixin, db.Model):
    """An administrator who can log in to /admin."""

    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<AdminUser {self.email}>"


# ---------------------------------------------------------------------------
# COURSE CATALOGUE
# ---------------------------------------------------------------------------
class Course(db.Model):
    """A course in the catalogue. Admin can add/edit/remove these."""

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(60), nullable=False)  # technology | academic | exam-prep | languages
    image = db.Column(db.String(255), default="courses/default.svg")
    short_description = db.Column(db.String(400))
    overview = db.Column(db.Text)
    who_its_for = db.Column(db.String(300))
    age_range = db.Column(db.String(50))
    level = db.Column(db.String(30))  # Beginner | Intermediate | Advanced | All Levels
    duration = db.Column(db.String(60))
    mode = db.Column(db.String(40))  # Online | Physical | Online & Physical
    price = db.Column(db.String(60), default="Contact for pricing")
    curriculum = db.Column(db.Text)  # newline-separated topics, rendered as a list
    outcomes = db.Column(db.Text)    # newline-separated outcomes
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship("Enrollment", backref="course", lazy="dynamic")

    def curriculum_list(self):
        return [line.strip() for line in (self.curriculum or "").splitlines() if line.strip()]

    def outcomes_list(self):
        return [line.strip() for line in (self.outcomes or "").splitlines() if line.strip()]

    def __repr__(self):
        return f"<Course {self.title}>"

class Program(db.Model):
    """
    Upcoming Programs — bootcamps, corporate training cohorts, holiday
    programmes, etc. Admin adds/edits/removes these from /admin/programs,
    and they're displayed on /programs using the same card style as courses.
    """

    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(255), default="courses/default.svg")
    short_description = db.Column(db.String(400))
    description = db.Column(db.Text)
    audience = db.Column(db.String(150))    # e.g. "Kids & Teens", "Corporate Teams"
    start_date = db.Column(db.String(100))  # free text, e.g. "11th August 2026" or "Rolling intake"
    duration = db.Column(db.String(60))
    mode = db.Column(db.String(40))         # Online | Physical | Online & Physical
    price = db.Column(db.String(60), default="Contact for pricing")
    highlights = db.Column(db.Text)         # newline-separated bullet points
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def highlights_list(self):
        return [line.strip() for line in (self.highlights or "").splitlines() if line.strip()]

    def __repr__(self):
        return f"<Program {self.title}>"
# ---------------------------------------------------------------------------
# REGISTRATIONS
# ---------------------------------------------------------------------------
class RegistrationStatus:
    """Shared status choices used by Student, ParentGuardian and TutorApplication."""
    PENDING = "Pending"
    CONTACTED = "Contacted"
    CONFIRMED = "Confirmed"
    ENROLLED = "Enrolled"
    REJECTED = "Rejected"

    CHOICES = [PENDING, CONTACTED, CONFIRMED, ENROLLED, REJECTED]


class Student(db.Model):
    """A learner who registered directly (adult / older teen)."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(30), unique=True, nullable=False, index=True)

    full_name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(300))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=True)
    course_name_snapshot = db.Column(db.String(150))  # preserved even if course is later deleted
    learning_mode = db.Column(db.String(40))
    preferred_schedule = db.Column(db.String(150))
    experience_level = db.Column(db.String(300))
    current_school = db.Column(db.String(200))
    referral_source = db.Column(db.String(150))
    additional_info = db.Column(db.Text)

    password_hash = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(20), default=RegistrationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", foreign_keys=[course_id])

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def __repr__(self):
        return f"<Student {self.registration_number} {self.full_name}>"


class ParentGuardian(db.Model):
    """A parent/guardian account - holds contact info; children are separate rows."""

    __tablename__ = "parents_guardians"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    whatsapp_number = db.Column(db.String(30))
    relationship_to_child = db.Column(db.String(60))
    address = db.Column(db.String(300))

    emergency_contact_name = db.Column(db.String(150))
    emergency_contact_phone = db.Column(db.String(30))
    emergency_contact_relationship = db.Column(db.String(60))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    children = db.relationship("Child", backref="parent", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ParentGuardian {self.full_name}>"


class Child(db.Model):
    """A child registered by a parent/guardian - this row carries the registration number."""

    __tablename__ = "children"

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents_guardians.id"), nullable=False)

    full_name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20))
    current_school = db.Column(db.String(200))
    grade_class = db.Column(db.String(100))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=True)
    course_name_snapshot = db.Column(db.String(150))
    learning_mode = db.Column(db.String(40))
    preferred_schedule = db.Column(db.String(150))
    experience_level = db.Column(db.String(300))
    learning_goals = db.Column(db.Text)
    additional_info = db.Column(db.Text)

    status = db.Column(db.String(20), default=RegistrationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", foreign_keys=[course_id])

    def __repr__(self):
        return f"<Child {self.registration_number} {self.full_name}>"


class TutorApplication(db.Model):
    """An application from someone wanting to teach at Dynamic Academy."""

    __tablename__ = "tutor_applications"

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(30), unique=True, nullable=False, index=True)

    # Personal information
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    whatsapp_number = db.Column(db.String(30))
    location = db.Column(db.String(150))
    gender = db.Column(db.String(20))

    # Professional information
    highest_qualification = db.Column(db.String(150))
    field_of_study = db.Column(db.String(150))
    years_of_experience = db.Column(db.String(50))
    subjects_courses = db.Column(db.String(300))
    technology_skills = db.Column(db.String(300))
    programming_languages = db.Column(db.String(300))
    age_groups = db.Column(db.String(200))
    preferred_mode = db.Column(db.String(60))
    availability = db.Column(db.String(200))
    expected_rate = db.Column(db.String(100))

    # Experience
    previous_institution = db.Column(db.String(200))
    certifications = db.Column(db.String(300))
    portfolio_url = db.Column(db.String(300))
    linkedin_url = db.Column(db.String(300))

    # Securely-stored uploaded documents (filenames only; files live outside
    # the public static folder - see config.UPLOAD_FOLDER)
    cv_filename = db.Column(db.String(255))
    certificate_filename = db.Column(db.String(255))

    status = db.Column(db.String(20), default=RegistrationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TutorApplication {self.application_number} {self.full_name}>"


# ---------------------------------------------------------------------------
# ENROLLMENT (link table joining a registration to a course, for reporting)
# ---------------------------------------------------------------------------
class Enrollment(db.Model):
    """
    Lightweight record of "someone wants to take this course", created
    alongside a Student or Child registration. Kept separate from Student/
    Child so future features (multiple courses per learner, payments) can
    build on it without changing the registration tables.
    """

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# CONTACT & NEWSLETTER
# ---------------------------------------------------------------------------
class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30))
    course_interest = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# BLOG (simple, admin-editable content could be added later; seeded for now)
# ---------------------------------------------------------------------------
class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(400))
    content = db.Column(db.Text)
    category = db.Column(db.String(60))
    image = db.Column(db.String(255), default="blog/default.svg")
    author = db.Column(db.String(120), default="Dynamic Academy Team")
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

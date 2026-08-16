"""
WTForms form definitions.

Each form here mirrors a database model and handles:
  - Which fields exist
  - Required/optional validation
  - Field-level validation (email format, matching passwords, etc.)

Templates render these with `{{ form.field_name(...) }}` and Flask-WTF
handles CSRF protection automatically for every form on this page.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import (
    StringField, TextAreaField, SelectField, DateField, IntegerField,
    PasswordField, BooleanField, SubmitField,
)
from wtforms.validators import (
    DataRequired, Email, Optional, Length, EqualTo, NumberRange, ValidationError, Regexp
)

GENDER_CHOICES = [("", "Select gender"), ("Male", "Male"), ("Female", "Female"), ("Prefer not to say", "Prefer not to say")]
LEARNING_MODE_CHOICES = [("", "Select mode"), ("Online", "Online"), ("Physical", "Physical"), ("Online & Physical", "Online & Physical")]

PHONE_REGEX = r"^\+?\d[\d\s\-()]{6,18}\d$"


def _phone_validator(message="Please enter a valid phone number."):
    return Regexp(PHONE_REGEX, message=message)


class StudentRegistrationForm(FlaskForm):
    """/student-register - for adults / older teens registering themselves."""

    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=150)])
    date_of_birth = DateField("Date of Birth", validators=[Optional()])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=1, max=120, message="Please enter a valid age.")])
    gender = SelectField("Gender", choices=GENDER_CHOICES, validators=[Optional()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    phone = StringField("Phone Number", validators=[DataRequired(), _phone_validator()])
    address = StringField("Address", validators=[Optional(), Length(max=300)])

    course = SelectField("Course", validators=[DataRequired(message="Please select a course.")], coerce=str)
    learning_mode = SelectField("Learning Mode", choices=LEARNING_MODE_CHOICES, validators=[DataRequired(message="Please select a learning mode.")])
    preferred_schedule = StringField("Preferred Class Schedule", validators=[Optional(), Length(max=150)])
    experience_level = TextAreaField("Previous Programming/Technology Experience", validators=[Optional(), Length(max=1000)])
    current_school = StringField("Current School/Institution", validators=[Optional(), Length(max=200)])
    referral_source = StringField("How did you hear about Dynamic Academy?", validators=[Optional(), Length(max=150)])
    additional_info = TextAreaField("Additional Information", validators=[Optional(), Length(max=1000)])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])

    agree_terms = BooleanField("I agree to the Dynamic Academy terms and privacy policy.", validators=[DataRequired(message="You must agree to the terms to continue.")])

    submit = SubmitField("Register as Student")


class ParentRegistrationForm(FlaskForm):
    """/parent-register - parent/guardian info + one child's info in a single submission."""

    # Parent/Guardian information
    parent_full_name = StringField("Parent/Guardian Full Name", validators=[DataRequired(), Length(max=150)])
    parent_email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    parent_phone = StringField("Phone Number", validators=[DataRequired(), _phone_validator()])
    parent_whatsapp = StringField("WhatsApp Number", validators=[Optional(), _phone_validator()])
    relationship_to_child = StringField("Relationship to Child", validators=[DataRequired(), Length(max=60)])
    parent_address = StringField("Address", validators=[Optional(), Length(max=300)])

    # Child information
    child_full_name = StringField("Child's Full Name", validators=[DataRequired(), Length(max=150)])
    child_date_of_birth = DateField("Date of Birth", validators=[Optional()])
    child_age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=1, max=25, message="Please enter a valid age.")])
    child_gender = SelectField("Gender", choices=GENDER_CHOICES, validators=[Optional()])
    child_school = StringField("Current School", validators=[Optional(), Length(max=200)])
    child_grade = StringField("Class/Grade", validators=[Optional(), Length(max=100)])

    course = SelectField("Course", validators=[DataRequired(message="Please select a course.")], coerce=str)
    learning_mode = SelectField("Learning Mode", choices=LEARNING_MODE_CHOICES, validators=[DataRequired(message="Please select a learning mode.")])
    preferred_schedule = StringField("Preferred Schedule", validators=[Optional(), Length(max=150)])
    experience_level = TextAreaField("Previous Experience", validators=[Optional(), Length(max=1000)])
    learning_goals = TextAreaField("Learning Goals", validators=[Optional(), Length(max=1000)])
    additional_info = TextAreaField("Additional Information", validators=[Optional(), Length(max=1000)])

    # Emergency contact
    emergency_contact_name = StringField("Emergency Contact Name", validators=[DataRequired(), Length(max=150)])
    emergency_contact_phone = StringField("Emergency Contact Phone", validators=[DataRequired(), _phone_validator()])
    emergency_contact_relationship = StringField("Relationship", validators=[DataRequired(), Length(max=60)])

    confirm_guardian = BooleanField("I confirm that I am the parent/guardian of the child.", validators=[DataRequired(message="Please confirm you are the parent/guardian.")])
    agree_terms = BooleanField("I agree to the Dynamic Academy terms and privacy policy.", validators=[DataRequired(message="You must agree to the terms to continue.")])

    submit = SubmitField("Register My Child")


class TutorApplicationForm(FlaskForm):
    """/tutor-application - tutor recruitment form with CV/certificate upload."""

    # Personal information
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=150)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    phone = StringField("Phone Number", validators=[DataRequired(), _phone_validator()])
    whatsapp_number = StringField("WhatsApp Number", validators=[Optional(), _phone_validator()])
    location = StringField("Location", validators=[DataRequired(), Length(max=150)])
    gender = SelectField("Gender", choices=GENDER_CHOICES, validators=[Optional()])

    # Professional information
    highest_qualification = StringField("Highest Qualification", validators=[DataRequired(), Length(max=150)])
    field_of_study = StringField("Field of Study", validators=[DataRequired(), Length(max=150)])
    years_of_experience = StringField("Years of Teaching Experience", validators=[DataRequired(), Length(max=50)])
    subjects_courses = StringField("Subjects/Courses You Teach", validators=[DataRequired(), Length(max=300)])
    technology_skills = StringField("Technology Skills", validators=[Optional(), Length(max=300)])
    programming_languages = StringField("Programming Languages", validators=[Optional(), Length(max=300)])
    age_groups = StringField("Age Groups You Can Teach", validators=[DataRequired(), Length(max=200)])
    preferred_mode = SelectField("Preferred Teaching Mode", choices=LEARNING_MODE_CHOICES, validators=[DataRequired(message="Please select a teaching mode.")])
    availability = StringField("Preferred Availability", validators=[Optional(), Length(max=200)])
    expected_rate = StringField("Expected Rate", validators=[Optional(), Length(max=100)])

    # Experience
    previous_institution = StringField("Previous Institution/Organization", validators=[Optional(), Length(max=200)])
    certifications = StringField("Professional Certifications", validators=[Optional(), Length(max=300)])
    portfolio_url = StringField("Portfolio/Website", validators=[Optional(), Length(max=300)])
    linkedin_url = StringField("LinkedIn Profile", validators=[Optional(), Length(max=300)])

    # Documents
    cv_file = FileField("CV/Resume", validators=[
        DataRequired(message="Please upload your CV/Resume."),
        FileAllowed(["pdf", "doc", "docx"], "Only PDF or Word documents are allowed."),
        FileSize(max_size=8 * 1024 * 1024, message="File must be smaller than 8MB."),
    ])
    certificate_file = FileField("Certificates", validators=[
        Optional(),
        FileAllowed(["pdf", "doc", "docx"], "Only PDF or Word documents are allowed."),
        FileSize(max_size=8 * 1024 * 1024, message="File must be smaller than 8MB."),
    ])

    confirm_accurate = BooleanField("I confirm that the information provided is accurate.", validators=[DataRequired(message="Please confirm the information is accurate.")])
    agree_terms = BooleanField("I agree to the Dynamic Academy tutor application terms.", validators=[DataRequired(message="You must agree to the terms to continue.")])

    submit = SubmitField("Submit Tutor Application")


class ContactForm(FlaskForm):
    """/contact form."""

    name = StringField("Full Name", validators=[DataRequired(), Length(max=150)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    phone = StringField("Phone Number", validators=[Optional(), _phone_validator()])
    course_interest = StringField("Course Interested In", validators=[Optional(), Length(max=150)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send Message")


class NewsletterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Subscribe")


class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class CourseForm(FlaskForm):
    """Admin: add/edit a course."""
    image = StringField("Image Path", validators=[Optional(), Length(max=255)])
    title = StringField("Course Title", validators=[DataRequired(), Length(max=150)])
    category = SelectField("Category", choices=[
        ("technology", "Technology & Digital Skills"),
        ("academic", "Academic Support"),
        ("exam-prep", "Examination Preparation"),
        ("languages", "Languages"),
    ], validators=[DataRequired()])
    short_description = StringField("Short Description", validators=[DataRequired(), Length(max=400)])
    overview = TextAreaField("Overview", validators=[Optional(), Length(max=2000)])
    who_its_for = StringField("Who It's For", validators=[Optional(), Length(max=300)])
    age_range = StringField("Age Range", validators=[Optional(), Length(max=50)])
    level = SelectField("Level", choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced"), ("All Levels", "All Levels")])
    duration = StringField("Duration", validators=[Optional(), Length(max=60)])
    mode = SelectField("Learning Mode", choices=LEARNING_MODE_CHOICES[1:], validators=[DataRequired()])
    price = StringField("Price", validators=[Optional(), Length(max=60)])
    curriculum = TextAreaField("Curriculum (one topic per line)", validators=[Optional()])
    outcomes = TextAreaField("Learning Outcomes (one per line)", validators=[Optional()])
    is_featured = BooleanField("Feature this course on the homepage")
    is_published = BooleanField("Published (visible on the website)", default=True)
    submit = SubmitField("Save Course")

class ProgramForm(FlaskForm):
    """Admin: add/edit an upcoming programme (bootcamps, corporate training, etc.)."""

    title = StringField("Programme Title", validators=[DataRequired(), Length(max=150)])
    short_description = StringField("Short Description", validators=[DataRequired(), Length(max=400)])
    description = TextAreaField("Full Description", validators=[Optional(), Length(max=2000)])
    audience = StringField("Audience", validators=[Optional(), Length(max=150)])
    start_date = StringField("Start Date", validators=[Optional(), Length(max=100)])
    duration = StringField("Duration", validators=[Optional(), Length(max=60)])
    mode = SelectField("Mode", choices=LEARNING_MODE_CHOICES[1:], validators=[DataRequired()])
    price = StringField("Price", validators=[Optional(), Length(max=60)])
    highlights = TextAreaField("Highlights (one per line)", validators=[Optional()])
    image = StringField("Image Path", validators=[Optional(), Length(max=255)])
    is_featured = BooleanField("Feature this programme on the homepage")
    is_published = BooleanField("Published (visible on the website)", default=True)
    submit = SubmitField("Save Programme")

class StatusUpdateForm(FlaskForm):
    """Small inline form admins use to change a registration's status."""
    status = SelectField("Status", choices=[(s, s) for s in
        ["Pending", "Contacted", "Confirmed", "Enrolled", "Rejected"]])
    submit = SubmitField("Update Status")

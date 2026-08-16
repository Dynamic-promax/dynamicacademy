"""
Tutor application, including secure CV/certificate upload.

Uploaded files are stored outside the public /static folder (see
config.UPLOAD_FOLDER) with randomised filenames, so they can never be
accessed by guessing a URL. Only a logged-in admin can download them,
via app/routes/admin.py's download route.
"""
from flask import Blueprint, render_template, redirect, url_for

from app.extensions import db
from app.forms import TutorApplicationForm
from app.models import TutorApplication
from app.utils.helpers import generate_registration_number, save_uploaded_file

tutor_bp = Blueprint("tutor", __name__)


@tutor_bp.route("/tutor-application", methods=["GET", "POST"])
def tutor_application():
    form = TutorApplicationForm()

    if form.validate_on_submit():
        cv_filename = save_uploaded_file(form.cv_file.data, subfolder="cv")
        certificate_filename = save_uploaded_file(form.certificate_file.data, subfolder="certificates")

        count_so_far = TutorApplication.query.count()
        app_number = generate_registration_number("TUT", count_so_far)

        application = TutorApplication(
            application_number=app_number,
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            whatsapp_number=form.whatsapp_number.data,
            location=form.location.data,
            gender=form.gender.data,
            highest_qualification=form.highest_qualification.data,
            field_of_study=form.field_of_study.data,
            years_of_experience=form.years_of_experience.data,
            subjects_courses=form.subjects_courses.data,
            technology_skills=form.technology_skills.data,
            programming_languages=form.programming_languages.data,
            age_groups=form.age_groups.data,
            preferred_mode=form.preferred_mode.data,
            availability=form.availability.data,
            expected_rate=form.expected_rate.data,
            previous_institution=form.previous_institution.data,
            certifications=form.certifications.data,
            portfolio_url=form.portfolio_url.data,
            linkedin_url=form.linkedin_url.data,
            cv_filename=cv_filename,
            certificate_filename=certificate_filename,
        )
        db.session.add(application)
        db.session.commit()

        return redirect(url_for("registration.success", kind="tutor", ref=app_number))

    return render_template("tutor_application.html", form=form)

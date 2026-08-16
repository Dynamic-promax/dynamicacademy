"""Contact form and newsletter signup."""
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request

from app.extensions import db
from app.forms import ContactForm, NewsletterForm
from app.models import ContactMessage, NewsletterSubscriber

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        db.session.add(ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data,
            course_interest=form.course_interest.data,
            message=form.message.data.strip(),
        ))
        db.session.commit()
        flash("Thank you! Your message has been received - our team will get back to you shortly.", "success")
        return redirect(url_for("contact.contact"))
    return render_template("contact.html", form=form)


@contact_bp.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    """Small AJAX endpoint used by the footer newsletter form."""
    form = NewsletterForm()
    if form.validate_on_submit():
        existing = NewsletterSubscriber.query.filter_by(email=form.email.data.strip().lower()).first()
        if not existing:
            db.session.add(NewsletterSubscriber(email=form.email.data.strip().lower()))
            db.session.commit()
        return jsonify(success=True, message="Subscribed successfully!")
    return jsonify(success=False, message="Please enter a valid email address."), 422

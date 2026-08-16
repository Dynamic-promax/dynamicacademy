"""
Core informational pages: home, about, kids, adults, online learning,
tutors (public listing), FAQ, blog.
"""
from flask import Blueprint, render_template

from app.models import Course, BlogPost, Program

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    featured_courses = Course.query.filter_by(is_published=True, is_featured=True).limit(6).all()
    featured_programs = Program.query.filter_by(is_published=True, is_featured=True).order_by(Program.created_at.desc()).limit(3).all()
    return render_template("home.html", featured_courses=featured_courses, featured_programs=featured_programs)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/kids")
def kids():
    kid_slugs = ["python-programming", "robotics", "game-development", "digital-skills", "artificial-intelligence", "web-development"]
    kid_courses = Course.query.filter(Course.slug.in_(kid_slugs), Course.is_published == True).all()
    return render_template("kids.html", courses=kid_courses)


@main_bp.route("/adults")
def adults():
    adult_slugs = ["python-programming", "artificial-intelligence", "web-development", "digital-skills", "graphics-design", "ai-content-creation"]
    adult_courses = Course.query.filter(Course.slug.in_(adult_slugs), Course.is_published == True).all()
    return render_template("adults.html", courses=adult_courses)


@main_bp.route("/online-learning")
def online_learning():
    return render_template("online_learning.html")


@main_bp.route("/tutors")
def tutors():
    return render_template("tutors.html")

@main_bp.route("/corporate")
def corporate():
    return render_template("corporate.html")


@main_bp.route("/faq")
def faq():
    faqs = [
        ("What age groups do you teach?", "We teach learners from children (age 10+) through teenagers to adults."),
        ("Do you offer online classes?", "Yes. Dynamic Academy offers fully online classes with live instructors and flexible schedules."),
        ("Do you offer physical classes?", "Yes. Selected courses are available physically at our location in Abuja."),
        ("Where is Dynamic Academy located?", "Apex Garden Estate, Kukwaba District, Abuja, Nigeria."),
        ("Do students need previous coding experience?", "No. Most of our technology courses are designed for complete beginners."),
        ("What courses do you offer?", "Technology, academic support, examination preparation (WAEC, NECO, JAMB, Cambridge) and language courses."),
        ("How do I register?", "Register as a student, register your child as a parent/guardian, or chat with us on WhatsApp."),
        ("How much do courses cost?", "Pricing varies by course - see individual course pages or contact us for a quote."),
        ("Do you offer weekend classes?", "Scheduling varies by course - contact us on WhatsApp to confirm availability."),
        ("Do you offer private tutoring?", "Yes, private/personalised sessions can be arranged for select courses."),
        ("Can my child join a technology class without previous experience?", "Absolutely - our programs welcome complete beginners."),
        ("How do I apply to become a tutor?", "Visit our Tutor Application page and submit your CV and details for review."),
    ]
    return render_template("faq.html", faqs=faqs)


@main_bp.route("/blog")
def blog():
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template("blog.html", posts=posts)


@main_bp.route("/blog/<slug>")
def blog_detail(slug):
    from flask import abort
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        abort(404)
    related = BlogPost.query.filter(
        BlogPost.category == post.category, BlogPost.slug != slug, BlogPost.is_published == True
    ).limit(3).all()
    return render_template("blog_detail.html", post=post, related=related)

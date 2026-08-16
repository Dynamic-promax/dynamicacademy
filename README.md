# Dynamic Academy — Website & Registration Platform

**Think. Learn. Create. Lead.**

A real, working education platform for Dynamic Academy (Abuja, Nigeria) built with **Python,
Flask, HTML, CSS and vanilla JavaScript** — no React, no Next.js, no build step. Everything here
runs with a plain Python virtual environment.

---

## 1. What's actually in here

This is a working application, not a mockup:

- **Real forms that save to a real database** — student registration, parent/guardian
  registration, tutor applications (with CV/certificate upload), and contact messages all write
  to SQLite via SQLAlchemy.
- **Real admin dashboard** — log in, see live counts, search/filter registrations, change
  registration status, add/edit/delete courses, securely download tutor CVs.
- **Real authentication** — password hashing (Werkzeug), session-based login (Flask-Login), CSRF
  protection on every form (Flask-WTF).
- **22 seeded courses** across Technology, Academic Support, Examination Preparation and
  Languages, each with its own detail page.
- Every route, every form submission, and the full admin flow (login, view data, update status,
  secure CV download, logout) has been tested end-to-end while building this project.

---

## 2. Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask |
| Database | SQLAlchemy ORM — SQLite for local dev, PostgreSQL-ready for production |
| Forms | Flask-WTF + WTForms (validation, CSRF) |
| Auth | Flask-Login + Werkzeug password hashing |
| Frontend | Plain HTML5 (Jinja2 templates) + CSS3 + vanilla JavaScript — no frameworks, no npm, no build step |
| Config | python-dotenv (`.env` file) |

---

## 3. Project structure

```
dynamic-academy-flask/
├── app/
│   ├── __init__.py          # App factory + CLI commands (init-db, create-admin, seed-courses)
│   ├── extensions.py        # db, csrf, login_manager objects
│   ├── models.py            # All database tables (SQLAlchemy models)
│   ├── forms.py             # All WTForms form definitions + validation rules
│   ├── seed_data.py         # The 22 courses + demo blog posts
│   ├── routes/
│   │   ├── main.py          # Home, About, Kids, Adults, Online Learning, Tutors, FAQ, Blog
│   │   ├── courses.py       # Course listing, course detail, "Enroll Now" chooser
│   │   ├── registration.py  # Student + Parent/Guardian registration
│   │   ├── tutor.py         # Tutor application (with file upload)
│   │   ├── contact.py       # Contact form + newsletter
│   │   ├── auth.py          # Admin login/logout
│   │   └── admin.py         # Admin dashboard, all list/detail/CRUD views
│   ├── templates/           # Jinja2 HTML templates (one per page, plus partials/ and admin/)
│   ├── static/
│   │   ├── css/              # tokens.css (design system variables) + components.css
│   │   ├── js/main.js        # Nav toggle, scroll reveal, counters, AJAX newsletter form
│   │   └── images/           # Placeholder SVG graphics (see section 10)
│   └── utils/
│       ├── academy.py        # SINGLE SOURCE OF TRUTH for academy name/phone/WhatsApp/address
│       └── helpers.py        # Registration number generator, secure file upload, WhatsApp links
├── instance/
│   ├── dynamic_academy.db    # SQLite database (created by `flask init-db`)
│   └── uploads/tutors/       # Tutor CVs/certificates — never publicly accessible
├── database/schema_notes.sql # Readable reference of the database schema
├── config.py                 # App configuration (reads from .env)
├── run.py                    # Entry point — `python run.py` starts the server
├── requirements.txt
├── .env.example
└── scripts_generate_placeholders.py  # One-off script that generated the placeholder images
```

---

## 4. Setup — Windows commands

Open **Command Prompt** or **PowerShell** in the project folder and run these in order:

```bat
:: 1. Create a virtual environment
python -m venv venv

:: 2. Activate it
venv\Scripts\activate

:: 3. Install dependencies
pip install -r requirements.txt

:: 4. Copy environment variables
copy .env.example .env

:: 5. Initialize the database (creates instance\dynamic_academy.db)
set FLASK_APP=run.py
flask init-db

:: 6. Create the admin account (uses ADMIN_EMAIL / ADMIN_PASSWORD from .env)
flask create-admin

:: 7. Seed the course catalogue (22 courses + demo blog posts)
flask seed-courses

:: 8. Run the application
python run.py
```

Then open **http://127.0.0.1:5000** in your browser. Admin dashboard: **http://127.0.0.1:5000/admin/login**

> On PowerShell, if `venv\Scripts\activate` is blocked, run PowerShell as Administrator once and
> execute `Set-ExecutionPolicy RemoteSigned`, then try again.

### macOS / Linux equivalent (for reference)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export FLASK_APP=run.py
flask init-db
flask create-admin
flask seed-courses
python run.py
```

---

## 5. Default admin login

Set in `.env` (copied from `.env.example`):

```
ADMIN_EMAIL=admin@dynamicacademy.ng
ADMIN_PASSWORD=ChangeThisPassword123!
```

**Change `ADMIN_PASSWORD` in `.env` before running `flask create-admin`**, or re-run
`flask create-admin` after changing it — it updates the existing admin's password if the account
already exists.

---

## 6. How the database works

- Tables are Python classes in `app/models.py` (SQLAlchemy models) — no separate SQL files to
  maintain by hand. `flask init-db` reads these classes and creates matching tables.
- Local development uses **SQLite** — a single file at `instance/dynamic_academy.db`. No server to
  install; it just works.
- **To reset the database** during development: stop the server, delete
  `instance/dynamic_academy.db`, then re-run `flask init-db`, `flask create-admin`, and
  `flask seed-courses`. This is destructive (all registrations are lost) — only do this in
  development.
- **To move to PostgreSQL for production**, see `database/schema_notes.sql` (the "Migrating to
  PostgreSQL" section at the bottom) — it's a one-line `DATABASE_URL` change, no code changes
  needed.

---

## 7. How registration works

1. A visitor browses `/courses`, opens a course, and clicks **Enroll Now**.
2. `/enroll/<course-slug>` asks: *"I am a Student"* or *"I am a Parent/Guardian"*.
3. They land on `/student-register` or `/parent-register` with `?course=<slug>` in the URL —
   the form pre-selects that course automatically (see `registration.py`, `preselected_slug`).
4. On submit, `app/forms.py` validates every field server-side (required fields, email format,
   phone format, password match, age range, checkbox consent). Errors are shown inline, next to
   each field.
5. On success, a row is saved to `students` or `parents_guardians` + `children`, a unique
   registration number is generated (`DA-STU-2026-0001` / `DA-PAR-2026-0001`), and the visitor is
   redirected to a real confirmation page showing that number.
6. Tutor applications work the same way at `/tutor-application`, plus a secure file upload for
   CV/certificates (see section 8).

## 8. How tutor file uploads are secured

- Files are validated (PDF/DOC/DOCX only, max 8MB) both in the browser (`accept` attribute) and
  server-side (`FileAllowed`, `FileSize` validators in `forms.py`).
- Uploaded files are renamed to a random string (`uuid4().hex`) before saving, so the original
  filename is never trusted and can't be used to guess other files.
- Files are stored in `instance/uploads/tutors/` — outside the `app/static/` folder, so Flask
  never serves them directly by URL.
- The only way to download a CV/certificate is `/admin/tutors/<id>/download/<cv|certificate>`,
  which is decorated with `@login_required` — verified in testing to redirect to the login page
  when accessed while logged out.

---

## 9. Where to edit everything

| What | File |
|---|---|
| **Academy name, phone, WhatsApp number, address, email, social links** | `app/utils/academy.py` — the single source of truth used by every template |
| **WhatsApp number specifically** | `whatsapp_number` in `app/utils/academy.py` (currently `2348119001010` / 08119001010, the registration line) |
| **WhatsApp message templates** | `WHATSAPP_MESSAGES` in `app/utils/academy.py` |
| **Courses** (add/edit/remove) | Easiest: log in to `/admin/courses` and use the UI. Or edit `app/seed_data.py` and re-run `flask seed-courses`. |
| **Homepage stats (students trained, etc.)** | `data-counter` values directly in `app/templates/home.html` — these are placeholders, update with real figures when available |
| **Colors / design tokens** | `app/static/css/tokens.css` — CSS custom properties at the top (`--color-royal-600`, `--color-gold-500`, spacing scale, etc.) |
| **Logo** | Replace `app/static/images/logo.svg` with the real Dynamic Academy logo (update the reference in `partials/navbar.html` and `partials/footer.html` if you rename the file) |
| **FAQ content** | `faqs` list in `app/routes/main.py` |
| **Blog posts** | `app/seed_data.py` under `BLOG_POSTS`, then re-run `flask seed-courses` |

---

## 10. Replacing placeholder images

No real photos or logo were supplied, so `scripts_generate_placeholders.py` generated 27
on-brand SVG placeholder graphics (course images, blog images, hero illustration, logo) in the
navy/royal-blue/gold palette — not stock photography, just enough so nothing is broken. Replace
any file under `app/static/images/` with a real photo (jpg/png/webp all work) — no code changes
needed, templates reference the path, not the format.

---

## 11. Security checklist (implemented)

- Passwords hashed with Werkzeug (`generate_password_hash` / `check_password_hash`) — never
  stored in plain text.
- CSRF protection on every form (Flask-WTF `CSRFProtect`), verified in testing — a request with a
  missing/invalid token is rejected with a 400 response.
- Server-side validation on every field (see `app/forms.py`) — never trusts the browser alone.
- Admin routes protected with `@login_required` (Flask-Login), verified to redirect
  unauthenticated requests to `/admin/login`.
- Tutor CVs stored outside the public static folder with randomized filenames.
- File upload type/size validation (`FileAllowed`, `FileSize`).
- SQL injection protection via SQLAlchemy's parameterized queries (no raw string-built SQL
  anywhere in the codebase).
- Secrets (`SECRET_KEY`, `ADMIN_PASSWORD`) read from `.env`, never hard-coded — `.env` is
  git-ignored.
- Session cookies set `HttpOnly` and `SameSite=Lax` (see `config.py`).

---

## 12. Running in production (brief guidance)

The built-in `python run.py` server is for development only. For production:

1. Install a production WSGI server: `pip install gunicorn` (Linux) or `pip install waitress`
   (Windows).
2. Run with: `gunicorn -w 4 -b 0.0.0.0:8000 run:app` (Linux) or
   `waitress-serve --port=8000 run:app` (Windows).
3. Put it behind a reverse proxy (Nginx, Caddy, or your host's built-in proxy) with HTTPS.
4. Switch `DATABASE_URL` to PostgreSQL (see section 6).
5. Set `FLASK_DEBUG=0` in your production `.env`.
6. Use a real, long, random `SECRET_KEY`.
7. Common beginner-friendly hosts that support Flask: Render, Railway, PythonAnywhere.

---

## 13. Future recommendations

- **Student/Instructor portals**: `/online-learning` already has "Coming Soon" placeholder cards.
  Add login for a `Student`/future `Instructor` model using the same Flask-Login pattern as admin.
- **Email notifications**: `app/routes/registration.py`, `tutor.py`, and `contact.py` are
  structured so adding `Flask-Mail` (or an API like SendGrid/Resend) after each
  `db.session.commit()` is a small, isolated change — the registration number and email address
  are already available at that point in the code.
- **Payments**: add a `payments` table (see the migration notes in `database/schema_notes.sql`)
  and integrate Paystack/Flutterwave against the existing `Enrollment` records.
- **Course video content / LMS**: extend the `Course` model with a `lessons` relationship.

---

## 14. Content honesty

No testimonials, statistics, instructor credentials, awards or partnerships were fabricated.
Homepage statistics are explicitly marked as placeholders in the template. Blog posts are marked
as demo content. Replace with real information before launch.

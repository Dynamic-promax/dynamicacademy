-- =====================================================================
-- DYNAMIC ACADEMY — DATABASE SCHEMA REFERENCE
-- =====================================================================
-- This file documents the schema that Flask-SQLAlchemy creates from
-- app/models.py (via `flask init-db`). You do NOT need to run this
-- file manually for SQLite - `flask init-db` builds it from the Python
-- models automatically. This file is a readable reference, and a
-- starting point if you migrate to PostgreSQL later (see README.md).
-- =====================================================================

CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    slug VARCHAR(160) UNIQUE NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(60) NOT NULL,          -- technology | academic | exam-prep | languages
    image VARCHAR(255),
    short_description VARCHAR(400),
    overview TEXT,
    who_its_for VARCHAR(300),
    age_range VARCHAR(50),
    level VARCHAR(30),
    duration VARCHAR(60),
    mode VARCHAR(40),                       -- Online | Physical | Online & Physical
    price VARCHAR(60),
    curriculum TEXT,                        -- newline-separated topics
    outcomes TEXT,                          -- newline-separated outcomes
    is_featured BOOLEAN,
    is_published BOOLEAN,
    created_at DATETIME
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    registration_number VARCHAR(30) UNIQUE NOT NULL,   -- DA-STU-2026-0001
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE,
    age INTEGER,
    gender VARCHAR(20),
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    address VARCHAR(300),
    course_id INTEGER REFERENCES courses(id),
    course_name_snapshot VARCHAR(150),
    learning_mode VARCHAR(40),
    preferred_schedule VARCHAR(150),
    experience_level VARCHAR(300),
    current_school VARCHAR(200),
    referral_source VARCHAR(150),
    additional_info TEXT,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20),                     -- Pending | Contacted | Confirmed | Enrolled | Rejected
    created_at DATETIME
);

CREATE TABLE parents_guardians (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    whatsapp_number VARCHAR(30),
    relationship_to_child VARCHAR(60),
    address VARCHAR(300),
    emergency_contact_name VARCHAR(150),
    emergency_contact_phone VARCHAR(30),
    emergency_contact_relationship VARCHAR(60),
    created_at DATETIME
);

CREATE TABLE children (
    id INTEGER PRIMARY KEY,
    registration_number VARCHAR(30) UNIQUE NOT NULL,   -- DA-PAR-2026-0001
    parent_id INTEGER NOT NULL REFERENCES parents_guardians(id),
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE,
    age INTEGER,
    gender VARCHAR(20),
    current_school VARCHAR(200),
    grade_class VARCHAR(100),
    course_id INTEGER REFERENCES courses(id),
    course_name_snapshot VARCHAR(150),
    learning_mode VARCHAR(40),
    preferred_schedule VARCHAR(150),
    experience_level VARCHAR(300),
    learning_goals TEXT,
    additional_info TEXT,
    status VARCHAR(20),
    created_at DATETIME
);

CREATE TABLE tutor_applications (
    id INTEGER PRIMARY KEY,
    application_number VARCHAR(30) UNIQUE NOT NULL,    -- DA-TUT-2026-0001
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    whatsapp_number VARCHAR(30),
    location VARCHAR(150),
    gender VARCHAR(20),
    highest_qualification VARCHAR(150),
    field_of_study VARCHAR(150),
    years_of_experience VARCHAR(50),
    subjects_courses VARCHAR(300),
    technology_skills VARCHAR(300),
    programming_languages VARCHAR(300),
    age_groups VARCHAR(200),
    preferred_mode VARCHAR(60),
    availability VARCHAR(200),
    expected_rate VARCHAR(100),
    previous_institution VARCHAR(200),
    certifications VARCHAR(300),
    portfolio_url VARCHAR(300),
    linkedin_url VARCHAR(300),
    cv_filename VARCHAR(255),               -- randomized filename; actual file lives outside /static
    certificate_filename VARCHAR(255),
    status VARCHAR(20),
    created_at DATETIME
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    student_id INTEGER REFERENCES students(id),
    child_id INTEGER REFERENCES children(id),
    created_at DATETIME
);

CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    course_interest VARCHAR(150),
    message TEXT NOT NULL,
    is_resolved BOOLEAN,
    created_at DATETIME
);

CREATE TABLE newsletter_subscribers (
    id INTEGER PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    subscribed_at DATETIME
);

CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY,
    slug VARCHAR(180) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    excerpt VARCHAR(400),
    content TEXT,
    category VARCHAR(60),
    image VARCHAR(255),
    author VARCHAR(120),
    is_published BOOLEAN,
    created_at DATETIME
);

-- ---------------------------------------------------------------------
-- MIGRATING TO POSTGRESQL
-- ---------------------------------------------------------------------
-- 1. pip install psycopg2-binary
-- 2. Set DATABASE_URL in .env to your Postgres connection string, e.g.:
--    DATABASE_URL=postgresql://username:password@localhost:5432/dynamic_academy
-- 3. Run: flask init-db   (creates the same tables in Postgres)
-- 4. Run: flask create-admin
-- 5. Run: flask seed-courses
-- No application code changes are required - SQLAlchemy handles the
-- dialect differences automatically.

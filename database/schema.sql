-- =====================================================================
-- DYNAMIC ACADEMY — REFERENCE SCHEMA (PostgreSQL-flavoured)
-- =====================================================================
-- You do NOT need to run this file by hand. In normal use, SQLAlchemy
-- creates these tables automatically from app/models.py when you run:
--     flask init-db
-- This file exists as a human-readable reference for the schema, and
-- as a starting point if you ever want to manage migrations directly
-- with raw SQL (e.g. inspecting the schema, or hand-writing a migration).
-- Column types shown here are the PostgreSQL equivalents of the
-- SQLAlchemy column types used in app/models.py.
-- =====================================================================

CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(160) UNIQUE NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(60) NOT NULL,
    image VARCHAR(255) DEFAULT 'courses/default.svg',
    short_description VARCHAR(400),
    overview TEXT,
    who_its_for VARCHAR(300),
    age_range VARCHAR(50),
    level VARCHAR(30),
    duration VARCHAR(60),
    mode VARCHAR(40),
    price VARCHAR(60) DEFAULT 'Contact for pricing',
    curriculum TEXT,
    outcomes TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    is_published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    registration_number VARCHAR(30) UNIQUE NOT NULL,
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
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE parents_guardians (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    whatsapp_number VARCHAR(30),
    relationship_to_child VARCHAR(60),
    address VARCHAR(300),
    emergency_contact_name VARCHAR(150),
    emergency_contact_phone VARCHAR(30),
    emergency_contact_relationship VARCHAR(60),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE children (
    id SERIAL PRIMARY KEY,
    registration_number VARCHAR(30) UNIQUE NOT NULL,
    parent_id INTEGER NOT NULL REFERENCES parents_guardians(id) ON DELETE CASCADE,
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
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE tutor_applications (
    id SERIAL PRIMARY KEY,
    application_number VARCHAR(30) UNIQUE NOT NULL,
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
    cv_filename VARCHAR(255),
    certificate_filename VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    student_id INTEGER REFERENCES students(id),
    child_id INTEGER REFERENCES children(id),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE contact_messages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    course_interest VARCHAR(150),
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE newsletter_subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    subscribed_at TIMESTAMP DEFAULT now()
);

CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(180) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    excerpt VARCHAR(400),
    content TEXT,
    category VARCHAR(60),
    image VARCHAR(255) DEFAULT 'blog/default.svg',
    author VARCHAR(120) DEFAULT 'Dynamic Academy Team',
    is_published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_students_reg_number ON students(registration_number);
CREATE INDEX idx_children_reg_number ON children(registration_number);
CREATE INDEX idx_tutor_app_number ON tutor_applications(application_number);
CREATE INDEX idx_courses_category ON courses(category);

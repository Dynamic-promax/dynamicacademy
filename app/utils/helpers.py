"""
Small reusable helper functions used across routes.
"""
import os
import uuid
from datetime import datetime
from urllib.parse import quote

from werkzeug.utils import secure_filename
from flask import current_app


def generate_registration_number(prefix: str, count_so_far: int) -> str:
    """
    Build a registration number like DA-STU-2026-0001.

    `count_so_far` should be the number of existing rows of this type
    (queried by the caller) - we add 1 and zero-pad to 4 digits. This is
    simple and readable rather than perfectly collision-proof under heavy
    concurrent load; for a small academy's registration volume this is
    more than sufficient, and the column has a UNIQUE constraint as a
    safety net (a retry-on-collision loop could be added later if needed).
    """
    year = datetime.utcnow().year
    sequence = str(count_so_far + 1).zfill(4)
    return f"DA-{prefix}-{year}-{sequence}"


def save_uploaded_file(file_storage, subfolder: str = "") -> str | None:
    """
    Safely save an uploaded file (e.g. a tutor's CV) to the private
    upload folder (NOT inside /static, so it can't be accessed by
    guessing a URL - only the protected admin download route can serve it).

    Returns the stored filename (not the full path) to save in the DB,
    or None if no file was provided.
    """
    if not file_storage or not file_storage.filename:
        return None

    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
    # Prefix with a UUID so two people uploading "cv.pdf" never collide
    # and so filenames can't be guessed.
    stored_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(folder, exist_ok=True)
    file_storage.save(os.path.join(folder, stored_name))
    return stored_name


def whatsapp_link(phone: str, message: str) -> str:
    """Build a wa.me deep link with a pre-filled, URL-encoded message."""
    return f"https://wa.me/{phone}?text={quote(message)}"

"""
Entry point for running the app locally.

Usage:
    python run.py
Then open http://127.0.0.1:5000 in your browser.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env if present

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)

"""SQLite data layer for Spendly.

get_db()   — open a connection to the project's SQLite file with
              row_factory and foreign key enforcement configured.
init_db()  — create the users/expenses tables if they don't exist yet.
seed_db()  — insert demo data once, for local development.
"""

import sqlite3
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

# expense_tracker.db lives at the project root (sibling of app.py),
# matching the .gitignore entry. __file__ is database/db.py, so go
# up one level from this file's directory.
DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    """Open a new SQLite connection with row access and FK enforcement."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't already exist. Safe to call repeatedly."""
    conn = get_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert demo data once. No-ops if users already exist."""
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
        if existing["count"] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        today = date.today()
        sample_expenses = [
            (user_id, 42.50, "Food", _day_in_current_month(today, 2), "Groceries"),
            (user_id, 15.00, "Transport", _day_in_current_month(today, 4), "Bus pass"),
            (user_id, 120.00, "Bills", _day_in_current_month(today, 5), "Electricity bill"),
            (user_id, 60.00, "Health", _day_in_current_month(today, 9), "Pharmacy"),
            (user_id, 25.99, "Entertainment", _day_in_current_month(today, 12), "Movie tickets"),
            (user_id, 80.00, "Shopping", _day_in_current_month(today, 15), "New shoes"),
            (user_id, 10.00, "Other", _day_in_current_month(today, 18), "Miscellaneous"),
            (user_id, 33.25, "Food", _day_in_current_month(today, 20), "Restaurant dinner"),
        ]
        conn.executemany(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_expenses,
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email):
    """Query user by email (case-insensitive). Returns dict or None."""
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?",
            (email.lower(),),
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def _day_in_current_month(today, day):
    """Return YYYY-MM-DD for `day` in today's month/year, clamped to today.

    Clamps to `today` itself if `day` would land in the future, so seed
    dates never appear "ahead" of the current date regardless of which
    day of the month the app is first run on.
    """
    day = min(day, today.day)
    return date(today.year, today.month, day).isoformat()

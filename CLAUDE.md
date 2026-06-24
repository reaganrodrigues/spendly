# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a Flask-based personal expense tracking web application. The codebase is structured for incremental development with placeholder routes for features students implement step-by-step. The app has a complete UI frontend with Jinja2 templates, responsive CSS, and JavaScript, but the backend features (auth, database, expense CRUD) are partially stubbed.

## Quick Commands

### Setup & Running

```bash
# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask development server (port 5001)
python app.py

# Initialize database (after students implement database/db.py)
python -c "from database.db import init_db; init_db()"
```

### Testing

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run with coverage
pytest --cov=.
```

### Linting & Code Quality

```bash
# Using Flask's built-in syntax checker
python -m py_compile app.py database/db.py

# Check imports
python -c "import app"
```

## Project Structure

### Core Files
- **app.py** — Flask application with all route definitions. Currently implements landing, login, register, terms, and privacy routes. Placeholder routes use step-based comments (e.g., "coming in Step 3").
- **database/db.py** — Students implement SQLite database functions here:
  - `get_db()` — returns a connection with row_factory and foreign keys enabled
  - `init_db()` — creates tables using CREATE TABLE IF NOT EXISTS
  - `seed_db()` — populates sample data for development
- **requirements.txt** — Python dependencies (Flask, werkzeug, pytest, pytest-flask)

### Frontend
- **templates/** — Jinja2 HTML templates
  - `base.html` — shared layout with navbar, footer, and block content areas
  - `landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html` — page templates
- **static/css/style.css** — single stylesheet with CSS variables for a consistent color scheme (accent: `#1a472a`, danger: `#c0392b`, paper/ink tones)
- **static/js/main.js** — JavaScript foundation; currently handles video modal on landing page; students add feature JS here

### Layout & Routing
All pages use the base template. Routes are plainly named:
- `/` → landing
- `/login`, `/register` → auth pages
- `/terms`, `/privacy` → legal pages
- Placeholder routes like `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` are stubbed with text comments

## Development Notes

### Incremental Development
The app is designed for step-by-step feature building. Each placeholder route includes a comment like "coming in Step N" to signal where students should implement features. Follow this pattern when adding new functionality.

### Database Design
The SQLite database will need:
- Users table (email, password hash, etc.)
- Expenses table (user_id, amount, category, date, description)
- Categories table (optional, for predefined categories)
Ensure foreign keys are enabled in `get_db()` by setting `PRAGMA foreign_keys = ON`.

### Frontend Patterns
- Color scheme uses CSS custom properties (`:root` in style.css); update these to change the entire app's palette
- All pages inherit from `base.html`, which provides navbar navigation and footer
- Links use `url_for()` to generate routes dynamically

### Flask Configuration
- Debug mode is enabled (`debug=True`); turn off in production
- Runs on `localhost:5001`
- Ensure `.env` (if used for secrets) is in `.gitignore` — already configured

## Common Workflows

**Adding a new page:**
1. Create a `.html` template in `templates/` that extends `base.html`
2. Add a route in `app.py` that calls `render_template()`
3. Link to it from navbar or other templates using `url_for()`

**Implementing a database feature:**
1. Write schema in `database/db.py` (create_tables or alter functions)
2. Add query functions (e.g., `insert_expense()`, `get_user_expenses()`)
3. Import and call from route handlers in `app.py`

**Adding styling:**
- Modify `static/css/style.css` directly; no build step required
- Reference the CSS variable names in `:root` for consistency (e.g., `color: var(--accent)`)

**Testing routes:**
- Use pytest-flask fixtures to test routes with a test client
- Example: test `GET /` returns 200 and renders landing.html

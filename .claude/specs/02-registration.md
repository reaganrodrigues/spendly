# Spec: Registration

## Overview

Implement user registration functionality that allows new users to create accounts with email and password. This feature enables the foundational authentication system required for all subsequent steps. Registration includes input validation, duplicate email checking, secure password hashing, and error handling with user-friendly feedback.

## Depends on

- Step 1: Database setup (users and expenses tables must exist with proper schema)

## Routes

- `GET /register` — Display registration form (already implemented, shows `register.html`)
- `POST /register` — Handle registration form submission, validate input, insert user into database, and redirect on success or re-render with errors — public

## Database changes

No database changes. The `users` table already exists from Step 1 with the required schema (id, name, email, password_hash, created_at).

## Templates

- **Modify:** `templates/register.html` — Add form error display section; form already exists, update to show validation errors below the form

## Files to change

- `app.py` — Add POST handler for `/register` route
- `templates/register.html` — Add error display section to show validation feedback

## Files to create

No new files.

## New dependencies

No new dependencies. Use `werkzeug.security.generate_password_hash` (already installed).

## Rules for implementation

- No SQLAlchemy or ORMs
- Use parameterised queries only — never string-format email or name into SQL
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values in new CSS
- All templates extend `base.html`
- Validate on server side (do not rely on HTML5 validation)
- Email must be unique; check before insert to provide clear error message
- Password must be at least 8 characters
- Name must not be empty
- Email must be a valid format (basic check: contains @ and .)
- On registration error, re-render the form with error messages (do not redirect)
- On registration success, redirect to `/login` with a success message (optional flash message)
- Use HTTP POST for form submission (not GET)

## Definition of done

- [ ] Form submission via POST to `/register` is handled without errors
- [ ] Valid registration (unique email, valid inputs) inserts user into database
- [ ] Duplicate email shows error message on the form (does not insert)
- [ ] Empty name shows error message on the form
- [ ] Invalid email format shows error message on the form
- [ ] Password shorter than 8 characters shows error message on the form
- [ ] Password is hashed with werkzeug before storing in database
- [ ] After successful registration, user is redirected to `/login`
- [ ] Error messages are displayed on the registration form without losing form data
- [ ] Form uses parameterised queries (no SQL string formatting)
- [ ] App starts without errors and register page is accessible

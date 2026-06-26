# Spec: Login and Logout

## Overview

Implement user login and logout functionality to complete the authentication system. Login validates email and password against stored credentials, establishes a session, and redirects to the dashboard. Logout terminates the session and returns the user to the landing page. Together, these features enable secure user session management and access control for protected routes.

## Depends on

- Step 1: Database setup (users table must exist)
- Step 2: Registration (users must be able to create accounts)

## Routes

- `GET /login` — Display login form (already implemented, shows `login.html`)
- `POST /login` — Handle login form submission, validate credentials, create session, and redirect on success or re-render with errors — public
- `GET /logout` — Destroy session and redirect to landing page — protected (requires login)

## Database changes

No database changes. The `users` table from Step 1 contains the required fields (id, email, password_hash).

## Templates

- **Modify:** `templates/login.html` — Add form error display section; form already exists, update to show validation errors below the form

## Files to change

- `app.py` — Add POST handler for `/login` and GET handler for `/logout` routes
- `templates/login.html` — Add error display section to show validation feedback

## Files to create

No new files.

## New dependencies

No new dependencies. Use Flask's built-in `session` object and `werkzeug.security.check_password_hash` (already installed).

## Rules for implementation

- Use Flask's `session` object to store user_id after successful login
- Check password with `werkzeug.security.check_password_hash`
- Use parameterised queries only — never string-format email into SQL
- Email check is case-insensitive (store lowercase in database and normalize on login)
- On login error, re-render the form with error message (do not redirect)
- On login success, redirect to `/dashboard` (or `/` for now if dashboard not yet implemented)
- `/logout` must check that user is logged in before destroying session
- After logout, redirect to `/` (landing page)
- Use HTTP POST for login form submission
- Display generic error message for invalid credentials (do not distinguish between invalid email and wrong password for security)
- Session should persist across page reloads but expire on browser close (use Flask default session settings)

## Definition of done

- [ ] Login form submission via POST to `/login` is handled without errors
- [ ] Valid credentials (email exists and password matches) create a session and redirect to dashboard
- [ ] Invalid email shows generic error message ("Invalid email or password")
- [ ] Invalid password shows generic error message ("Invalid email or password")
- [ ] Empty email shows error message on the form
- [ ] Empty password shows error message on the form
- [ ] After successful login, user_id is stored in session
- [ ] Error messages are displayed on the login form without losing form data
- [ ] Form uses parameterised queries (no SQL string formatting)
- [ ] `/logout` redirects to landing page and destroys session
- [ ] `/logout` cannot be accessed or only works when user is logged in (401 or redirect to login)
- [ ] After logout, user cannot access protected routes
- [ ] App starts without errors and login page is accessible
- [ ] Password is checked with werkzeug.security.check_password_hash

# Flask User Management — Corrected Quickstart and Notes

This file corrects and clarifies the original README so examples run in this repo.

Quick Setup (cross-platform)

1. Create a Python virtual environment and activate it

   Bash / macOS / WSL

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   PowerShell (Windows)

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. App run options

   Option A — use flask CLI (recommended to pass host/port):

   Bash / PowerShell

   ```bash
   # On Windows PowerShell: $env:FLASK_APP = 'app.py'
   # On bash: export FLASK_APP=app.py
   flask run --host=0.0.0.0 --port=8080
   ```

   Option B — run script directly (default host/port)

   ```bash
   python app.py
   # Default: 127.0.0.1:5000 (app.py currently calls app.run(debug=True))
   ```

What changed vs the original README
----------------------------------

- Correct routes:
  - Register: `GET/POST /register` (template: `templates/register.html`)
  - Login: `GET/POST /login` (template: `templates/login.html`)
  - Dashboard: `GET /dashboard` (access requires login)

- There are no endpoints named `/signup`, `/signin`, `/profile`.
- There are no JSON API endpoints at `/api/register` or `/api/login` in this repository.
- Database file used by the app (unless overridden) is `app.db` at the repo root, not `data/database.sqlite3`.
- CSRF / Secret:
  - The app uses `app.config['SECRET_KEY']` (set in `app.py`). If you want to set the secret via an environment variable, add code to load FLASK_SECRET into app.config['SECRET_KEY'].

Validation rules (actual behavior)
---------------------------------

- Email: REQUIRED and unique
- Password: minimum length 6 characters (enforced by WTForms in `auth.py`)

Notes for contributors
----------------------
- If you want to expose JSON APIs under `/api/*` or use server-side Redis sessions, implement those backends and update the corrected README accordingly.

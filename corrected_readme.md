# Flask User Management Tutorial (Corrected)

This project provides a simple Flask-based user registration and login app.

Quick start (Unix/macOS):

```bash
# Create a Python virtual environment in project root
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the app
python app.py --host=0.0.0.0 --port=8080
```

Quick start (Windows PowerShell):

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python app.py --host=0.0.0.0 --port=8080
```

Notes (actual application behavior):

- Routes implemented in code:
  - GET/POST `/register` — register new user (fields: `username`, `email`, `password`)
  - GET/POST `/login` — login (fields: `username`, `password`)
  - GET `/logout` — logout
  - GET `/dashboard` — user dashboard (login required)
- The application uses `app.config['SECRET_KEY']` for CSRF/session secret. You can set this via environment variable when starting the app:
  - Linux/macOS: `FLASK_SECRET=supersecrete python app.py`
  - Windows PowerShell: `$env:FLASK_SECRET='supersecrete'; python app.py`
- Database file used by application: `app.db` in project root (SQLite)
- Password min length is enforced at 6 characters by forms
- Email is required by the Register form
- The README's `/api/register` and `/api/login` endpoints are not implemented in this project; only the web forms exist

Testing:

- Tests use pytest. To run tests:

```bash
# assuming virtualenv activated and requirements installed
pytest -q
```

Defects found during verification are documented in `defects.txt`. This corrected README updates commands and expected behavior to match the current codebase.

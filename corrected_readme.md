# Flask User Management — Corrected Quick Start

This document is the corrected README that reflects the actual implementation and working commands.

Prerequisites
- Python 3.10+ (create a virtual environment before installing packages)

Setup (Unix / Bash)
```bash
# Create a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

Setup (Windows / PowerShell)
```powershell
# Create a Python virtual environment
python -m venv .venv
.venv\Scripts\Activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

Run the app (recommended: use the flask CLI)
```bash
# Set FLASK_APP and run with host and port
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_SECRET="your-secret-key"
flask run --host=0.0.0.0 --port=8080
```
PowerShell:
```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
$env:FLASK_SECRET = 'your-secret-key'
flask run --host=0.0.0.0 --port=8080
```

Alternative: run directly with python and specify host/port (works with the included CLI flags):
```
python app.py --host=0.0.0.0 --port=8080
```

App routes (corrected)
- GET /register — Registration form (fields: username, email, password). Note: there is no confirm_password field in the current implementation.
- POST /register — Handles registration via HTML form.
- GET /login — Login form (username, password).
- POST /login — Login via HTML form.
- GET /dashboard — Dashboard (login required).
- GET /logout — Log out.

Notes and behavior
- The API endpoints under /api (e.g., /api/register, /api/login) are not implemented in this project.
- Password minimum length is 6 characters (validated by WTForms in the registration form).
- Email is required and must be unique per account.
- Default SQLite DB file: app.db at project root. You can change this in app.config['DATABASE'].
- SECRET_KEY is read from the FLASK_SECRET environment variable if set, otherwise a default placeholder is used. Configure FLASK_SECRET for production.
- Sessions are the default Flask sessions (not stored in Redis by default).

Tests
- Run tests with pytest (the project includes tests under tests/). Use the provided run_tests scripts.

Contact
- This project is a simple tutorial app; see defects.txt for the complete list of documentation mismatches found and reproduction steps.

# Flask Login Sample (Corrected)

A minimal Flask app with username/email registration, login, dashboard, and logout using `flask-login`, `flask-wtf`, and SQLite.

## Prerequisites
- Python 3.10+ (tested on 3.13)
- (Optional) Bash or PowerShell for helper scripts

## Setup

### One-liner scripts
- **PowerShell**
  ```powershell
  .\setup.ps1
  ```
- **Bash**
  ```bash
  ./setup.sh
  ```

### Manual steps
```powershell
# Create venv
python -m venv .venv
. .\.venv\Scripts\activate

# Install deps
pip install -r requirements.txt
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app
```powershell
. .\.venv\Scripts\activate
python app.py
```
Server starts at **http://127.0.0.1:5000** (host/port are hardcoded in `app.py`).

## Usage
- **Register**: `GET/POST /register`
  - Fields: `username` (required, unique, 3–32 chars), `email` (required, unique), `password` (required, 6–128 chars)
  - Successful registration logs you in and redirects to `/dashboard`.
- **Login**: `GET/POST /login`
  - Fields: `username`, `password`
- **Dashboard**: `GET /dashboard` (requires login)
- **Logout**: `GET /logout`

> **Not implemented**: `/signup`, `/signin`, `/profile`, `/api/register`, `/api/login`

## Configuration
- **Secret key**: Update `app.config['SECRET_KEY']` in `app.py` for CSRF/session protection.
- **Database**: SQLite file at `app.db`. Change `app.config['DATABASE']` to relocate.

## Testing
Run the pytest suite:
```powershell
. .\.venv\Scripts\activate
python -m pytest
```
Or use scripts:
- PowerShell: `./run_tests.ps1`
- Bash: `./run_tests.sh`

## Troubleshooting
- Delete `app.db` to reset users.
- Ensure `email-validator` is installed (included in `requirements.txt`).
- If imports fail in tests, run from project root so `app.py` is on `PYTHONPATH`.

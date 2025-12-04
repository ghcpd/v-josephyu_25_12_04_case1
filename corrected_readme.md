# Flask User Management — Corrected Quickstart

This project provides a small Flask app with registration and login.

Setup (Windows PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
```

Setup (Unix / Bash):

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run the app:

```
python app.py
```

Routes:
- `/register` — register via form (fields: `username`, `email`, `password`)
- `/login` — login via form (fields: `username`, `password`)
- `/logout` — logout

Notes:
- The README originally referenced `/signup` and `/signin` and `/api/*` endpoints; the actual routes are `/register` and `/login`. The app does not implement `/api/register` or `/api/login`.
- Templates include CSRF protection — tests disable it via `WTF_CSRF_ENABLED = False`.
- Database file is controlled by `app.config['DATABASE']` and defaults to `app.db`.

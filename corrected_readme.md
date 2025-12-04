# Flask User Management Application - CORRECTED README

This is a corrected version of the README with accurate documentation matching the actual implementation.

## From Scratch Setup

### Bash/Linux/macOS:
```bash
# Create a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### PowerShell (Windows):
```powershell
# Create a Python virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Default Server (Recommended for Development)
```bash
python app.py
```
This starts the Flask development server on `http://127.0.0.1:5000`

### Option 2: Using Flask CLI for Custom Host/Port
```bash
# Set FLASK_APP environment variable first
export FLASK_APP=app.py          # Linux/macOS
set FLASK_APP=app.py             # Windows CMD
$env:FLASK_APP = "app.py"        # PowerShell

# Run with Flask CLI
flask run --host=0.0.0.0 --port=8080
```

**Note:** Direct CLI arguments to `python app.py` are NOT supported. Use Flask CLI as shown above for custom host/port.

## Tutorial: Register and Login

1. **Register a user** at `/register` with fields:
   - `username` (3-32 characters)
   - `email` (valid email format, required)
   - `password` (6-128 characters)

2. **Login** at `/login` with:
   - `username`
   - `password`

3. **Access the dashboard** at `/dashboard` (only available when logged in)

4. **Logout** via the logout button on the dashboard

## API Reference

**Note:** REST API endpoints (`/api/register`, `/api/login`) are NOT currently implemented. 
Use web forms at `/register` and `/login` for user authentication.

Current web routes:
- GET `/register` - Display registration form
- POST `/register` - Submit registration form
- GET `/login` - Display login form
- POST `/login` - Submit login form
- GET `/dashboard` - User dashboard (requires login)
- GET `/logout` - Logout user

## Configuration

### Environment Variables

#### SECRET_KEY (CSRF Protection)
Currently uses hardcoded default. For production:

```python
# Modify app.py:
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

Then set environment variable:
```bash
export FLASK_SECRET="your-secret-key"        # Linux/macOS
set FLASK_SECRET=your-secret-key             # Windows CMD
$env:FLASK_SECRET = "your-secret-key"        # PowerShell
```

### Database Configuration

The application uses SQLite database at: `app.db` (project root)

**Note:** README previously documented `data/database.sqlite3` but actual implementation uses `app.db`

To change database path, modify `app.py`:
```python
app.config['DATABASE'] = 'path/to/your/database.db'
```

## Authentication Rules

### Password Requirements
- **Minimum length:** 6 characters
- **Maximum length:** 128 characters

**Note:** README previously claimed minimum was 3, actual minimum is 6.

### Email Requirements
- **Required:** Yes (despite earlier documentation stating optional)
- **Format:** Must be valid email address
- **Uniqueness:** Each user must have unique email

### Username Requirements
- **Minimum length:** 3 characters
- **Maximum length:** 32 characters
- **Uniqueness:** Required (enforced by database)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
```

## Form Fields

### Registration Form
```
- Username (required, 3-32 chars)
- Email (required, valid email format)
- Password (required, 6-128 chars)
- Submit button

NOTE: There is NO "confirm password" field despite README mentioning it
```

### Login Form
```
- Username (required)
- Password (required)
- Submit button
```

## Common Issues and Solutions

### Issue 1: "405 Method Not Allowed"
**Cause:** Trying to POST to GET-only routes or vice versa
**Solution:** Use the HTML forms at `/register` and `/login`

### Issue 2: "Invalid email" validation error
**Cause:** Email field was previously marked optional in docs but is required
**Solution:** Provide a valid email address

### Issue 3: Password too short
**Cause:** Entering password with less than 6 characters
**Solution:** Use at least 6 characters for password

### Issue 4: Port already in use
**Cause:** Port 5000 is already in use
**Solution:** Use Flask CLI with custom port: `flask run --port=8081`

### Issue 5: "Working outside of application context"
**Cause:** Running code that needs Flask app context outside request/CLI
**Solution:** Use `with app.app_context():`

## Session Management

### Current Implementation
- Sessions stored in client-side signed cookies
- Default Flask session mechanism (not Redis)

**Note:** Documentation previously mentioned "Sessions are stored server-side in Redis" but Redis is NOT integrated.

## Missing Features (Not Implemented)

The following features mentioned in original README are NOT implemented:
1. ❌ REST API endpoints (`/api/register`, `/api/login`)
2. ❌ `/profile` route (use `/dashboard` instead)
3. ❌ `/signin` route (use `/login` instead)
4. ❌ `/signup` route (use `/register` instead)
5. ❌ Redis session storage
6. ❌ Password confirmation field
7. ❌ Optional email field
8. ❌ CLI argument parsing (--host, --port) directly on `python app.py`

## Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=.
```

### Manual Testing Checklist
- [ ] Navigate to http://localhost:5000/register
- [ ] Create new account with valid credentials
- [ ] Verify email validation (try without @)
- [ ] Navigate to http://localhost:5000/login
- [ ] Login with created credentials
- [ ] View dashboard at http://localhost:5000/dashboard
- [ ] Verify logout button works
- [ ] Verify attempting to access /dashboard while logged out redirects to /login

## Deployment

### For Production:
1. Set secure `FLASK_SECRET` environment variable
2. Set `DEBUG=False` in app.py
3. Use production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
4. Use HTTPS
5. Configure proper database (consider PostgreSQL instead of SQLite)

## Project Structure
```
.
├── app.py                 # Main Flask application
├── auth.py               # Authentication routes and forms
├── models.py             # User model and database functions
├── requirements.txt      # Python dependencies
├── templates/
│   ├── base.html        # Base template with Bootstrap CSS
│   ├── login.html       # Login form
│   ├── register.html    # Registration form
│   └── dashboard.html   # User dashboard
└── app.db               # SQLite database (created on first run)
```

## Dependencies

See `requirements.txt` for full list. Key packages:
- Flask==3.0.0 - Web framework
- Flask-Login==0.6.3 - User session management
- Flask-WTF==1.2.1 - Form protection and CSRF
- WTForms==3.1.2 - Form validation
- Werkzeug==3.0.1 - WSGI utilities
- email_validator==2.2.0 - Email validation
- pytest - Testing framework

## Version Information

- Python: 3.8+
- Flask: 3.0.0
- Last Updated: December 2025

## Corrections Summary

This corrected README fixes 15+ defects from the original documentation including:
- Accurate route names (/login, /register, /dashboard)
- Correct password minimum length (6, not 3)
- Email is required (not optional)
- CLI argument limitations (must use Flask CLI)
- Accurate database path (app.db, not data/database.sqlite3)
- Removal of non-existent features (Redis, API endpoints, /profile)
- Proper environment setup instructions

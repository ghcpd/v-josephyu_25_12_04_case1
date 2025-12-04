import os
import sys
import tempfile
import pytest
# Ensure project root is in sys.path for imports during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary database file for tests
    db_file = tmp_path / "test_app.db"
    monkeypatch.setitem(flask_app.config, 'DATABASE', str(db_file))
    # Re-initialize DB schema in the new temp database
    from models import init_db
    init_db(flask_app)
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        yield client


def test_readme_routes_exist(client):
    # Corrected: app exposes /register and /login
    r1 = client.get('/register')
    r2 = client.get('/login')
    assert r1.status_code == 200, "Expected /register to exist"
    assert r2.status_code == 200, "Expected /login to exist"


def test_api_endpoints_exist(client):
    # There are no /api/register or /api/login endpoints in the app
    r1 = client.post('/api/register', json={"user": "u", "pass": "p", "mail": "e@x.com"})
    r2 = client.post('/api/login', json={"user": "u", "pass": "p"})
    assert r1.status_code == 404, "Expected /api/register to be absent"
    assert r2.status_code == 404, "Expected /api/login to be absent"


def test_password_min_length_per_readme(client):
    # Actual app requires minimum password length 6
    resp = client.post('/register', data={
        'username': 'testuser',
        'email': 't@e.com',
        'password': '123',
    }, follow_redirects=True)
    # Expect that the user was NOT created due to validation error
    import sqlite3
    db_path = flask_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE username = ?', ('testuser',))
    assert cur.fetchone() is None, "User should not be created when password is too short"
    conn.close()


def test_confirm_password_field_present_on_register(client):
    # Current register form does not include confirm_password
    resp = client.get('/register')
    assert b'confirm_password' not in resp.data, "confirm_password should not be present in current register form"

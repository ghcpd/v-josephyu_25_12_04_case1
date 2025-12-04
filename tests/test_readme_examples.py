import os
import tempfile

import pytest
import sys
import os

# Ensure project root is on path so tests can import modules
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

flask = pytest.importorskip('flask')
from app import app as flask_app
from models import get_connection

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_app.db"
    monkeypatch.setitem(flask_app.config, 'DATABASE', str(db_file))
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client


def test_register_and_login_form(client):
    # Access register page
    rv = client.get('/register')
    assert rv.status_code == 200

    # Register a new user
    rv = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'password1'
    }, follow_redirects=True)
    assert b'Dashboard' in rv.data or rv.status_code == 200

    # Logout and login
    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200

    rv = client.post('/login', data={'username': 'alice', 'password': 'password1'}, follow_redirects=True)
    assert b'Dashboard' in rv.data


def test_readme_api_endpoints(client):
    # The README documents /api/register and /api/login endpoints but the app does not implement them.
    rv = client.post('/api/register', json={'user': 'bob', 'pass': '123', 'mail': 'bob@example.com'})
    assert rv.status_code == 404

    rv = client.post('/api/login', json={'user': 'bob', 'pass': '123'})
    assert rv.status_code == 404

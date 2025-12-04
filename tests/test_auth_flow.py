import os
import tempfile

import pytest

from app import app as flask_app
from models import init_db, get_connection


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create a temp db file and configure the app to use it
    db_file = tmp_path / "test_app.db"
    monkeypatch.setitem(flask_app.config, 'DATABASE', str(db_file))
    # disable CSRF for tests
    monkeypatch.setitem(flask_app.config, 'WTF_CSRF_ENABLED', False)
    init_db(flask_app)
    with flask_app.test_client() as client:
        yield client


def test_register_login_logout_flow(client):
    # Register user
    resp = client.post('/register', data={'username': 'alice', 'email': 'alice@example.com', 'password': 'password'}, follow_redirects=False)
    # Successful registration should redirect to dashboard
    assert resp.status_code == 302 or resp.status_code == 301

    # Follow redirect and check dashboard content
    follow = client.get('/dashboard')
    assert b'Hello' in follow.data and b'alice' in follow.data

    # Logout
    resp2 = client.get('/logout', follow_redirects=False)
    assert resp2.status_code in (302, 301)

    # Login again with correct credentials
    resp3 = client.post('/login', data={'username': 'alice', 'password': 'password'}, follow_redirects=False)
    assert resp3.status_code in (302, 301)

    # Attempt duplicate username registration
    resp4 = client.post('/register', data={'username': 'alice', 'email': 'alice2@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Username is already taken' in resp4.data

    # Attempt duplicate email registration
    resp5 = client.post('/register', data={'username': 'alice2', 'email': 'alice@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Email is already registered' in resp5.data

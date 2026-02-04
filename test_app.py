import os
import tempfile
import pytest
from app import app as flask_app
from models import init_db, get_connection


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary database file
    db_file = tmp_path / "test_app.db"
    flask_app.config['TESTING'] = True
    # Disable CSRF for tests
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SECRET_KEY'] = 'test-secret-for-csrf'
    flask_app.config['DATABASE'] = str(db_file)
    # Ensure DB initialized
    init_db(flask_app)

    with flask_app.test_client() as client:
        yield client


def test_register_and_login_flow(client):
    # Register new user via form endpoint
    resp = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 's3cret'
    }, follow_redirects=True)
    assert resp.status_code == 200
    # After registration, user is redirected to dashboard; check welcome message
    assert b'Hello' in resp.data and b'alice' in resp.data

    # Logout
    resp = client.get('/logout', follow_redirects=True)
    assert resp.status_code == 200

    # Login with correct password
    resp = client.post('/login', data={
        'username': 'alice',
        'password': 's3cret'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Hello' in resp.data and b'alice' in resp.data


def test_api_register_and_login(client):
    # API endpoints do not exist per code; this test verifies behavior
    resp = client.post('/api/register', json={
        'user': 'bob',
        'pass': 'pw123',
        'mail': 'bob@example.com'
    })
    # Expect 404 as README claims endpoints exist but code does not implement them
    assert resp.status_code == 404

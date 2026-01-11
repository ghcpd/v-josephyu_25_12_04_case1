import os
import pytest

from app import app as flask_app


@pytest.fixture(autouse=True)
def no_env_flask_secret(monkeypatch):
    # Ensure FLASK_SECRET isn't set so behavior is deterministic
    monkeypatch.delenv('FLASK_SECRET', raising=False)
    # Disable CSRF so tests can POST forms without tokens
    monkeypatch.setitem(flask_app.config, 'WTF_CSRF_ENABLED', False)
    yield


def test_documented_endpoints_missing():
    client = flask_app.test_client()

    # README documents /signup, /signin and /profile but the app uses /register and /login
    for missing in ['/signup', '/signin', '/profile']:
        resp = client.get(missing)
        assert resp.status_code == 404, f"Expected 404 for {missing}, got {resp.status_code}"


def test_register_and_login_routes_exist():
    client = flask_app.test_client()
    assert client.get('/register').status_code == 200
    assert client.get('/login').status_code == 200


def test_api_endpoints_absent():
    client = flask_app.test_client()
    # README claims API endpoints under /api; not implemented
    assert client.post('/api/register').status_code in (404, 405)
    assert client.post('/api/login').status_code in (404, 405)


def test_config_db_and_secret_defaults():
    # README claims DB at data/database.sqlite3 and FLASK_SECRET env var — neither are used by code
    assert flask_app.config.get('DATABASE') == 'app.db'
    assert 'FLASK_SECRET' not in flask_app.config


def test_password_and_email_validation_on_register():
    client = flask_app.test_client()

    # Short password should not validate (code requires >=6)
    resp = client.post('/register', data={'username': 'bob', 'email': 'bob@example.com', 'password': '123'}, follow_redirects=True)
    assert resp.status_code == 200
    # the form should re-render and show registration page (validation failed) — exact wording may vary
    assert b'User Registration' in resp.data

    # Missing email should produce a validation error (code requires email)
    resp2 = client.post('/register', data={'username': 'bob2', 'email': '', 'password': 's3curepass'}, follow_redirects=True)
    assert resp2.status_code == 200
    # Expect an error about the email field not being a valid email or being required
    assert b'Email' in resp2.data

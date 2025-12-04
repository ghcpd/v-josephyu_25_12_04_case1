import sys
import os
import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

flask = pytest.importorskip('flask')
from app import app as flask_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_app.db"
    monkeypatch.setitem(flask_app.config, 'DATABASE', str(db_file))
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client


def test_register_page_and_login(client):
    rv = client.get('/register')
    assert rv.status_code == 200

    rv = client.post('/register', data={'username': 'carol', 'email': 'carol@example.com', 'password': 'passw0rd'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Dashboard' in rv.data

    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200

    rv = client.post('/login', data={'username': 'carol', 'password': 'passw0rd'}, follow_redirects=True)
    assert b'Dashboard' in rv.data

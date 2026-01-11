import sys
import os
import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

pytest.importorskip('werkzeug')

from models import init_db, get_connection, User
from app import app as flask_app


def test_create_and_retrieve_user(tmp_path, monkeypatch):
    db_file = tmp_path / "test_app.db"
    monkeypatch.setitem(flask_app.config, 'DATABASE', str(db_file))

    init_db(flask_app)
    conn = get_connection(flask_app)
    user = User.create(conn, 'bob', 'securepass', 'bob@example.com')
    assert user.id is not None

    fetched = User.get_by_username(conn, 'bob')
    assert fetched is not None
    assert fetched.username == 'bob'

    assert fetched.verify_password('securepass')
    conn.close()

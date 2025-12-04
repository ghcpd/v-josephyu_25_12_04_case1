import os
import sys
import tempfile
import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app as flask_app
from models import init_db


@pytest.fixture
def app():
    # Use a temporary file-based SQLite DB to allow multiple connections
    fd, db_path = tempfile.mkstemp(prefix="test_app_", suffix=".db")
    os.close(fd)

    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret-key",
        DATABASE=db_path,
    )
    init_db(flask_app)

    yield flask_app

    try:
        os.remove(db_path)
    except OSError:
        pass


@pytest.fixture
def client(app):
    return app.test_client()

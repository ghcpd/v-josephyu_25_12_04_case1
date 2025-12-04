import os
import importlib


def test_secret_key_from_env(monkeypatch):
    # Ensure that FLASK_SECRET environment variable sets SECRET_KEY in app
    monkeypatch.setenv('FLASK_SECRET', 'env-secret-xyz')
    # Reload the app module to pick up env var
    import app as app_module
    importlib.reload(app_module)
    assert app_module.app.config['SECRET_KEY'] == 'env-secret-xyz'
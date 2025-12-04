import pytest


doc_endpoints = [
    ("GET", "/signup"),
    ("GET", "/signin"),
    ("GET", "/profile"),
    ("POST", "/api/register"),
    ("POST", "/api/login"),
]


@pytest.mark.parametrize("method, path", doc_endpoints)
def test_readme_documented_endpoints_do_not_exist(method, path, client):
    resp = getattr(client, method.lower())(path)
    assert resp.status_code == 404

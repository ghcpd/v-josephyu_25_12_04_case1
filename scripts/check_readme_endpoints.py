import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

client = app.test_client()

def hit(method: str, url: str, **kwargs):
    func = getattr(client, method.lower())
    try:
        resp = func(url, **kwargs)
        print(f"{method} {url} -> {resp.status_code}")
        ct = resp.headers.get('Content-Type', '')
        if 'json' in ct:
            try:
                print(resp.get_json())
            except Exception:
                print(resp.data.decode(errors='ignore'))
        else:
            # print a short preview for HTML/text
            data = resp.data.decode(errors='ignore')
            print(data[:200].replace('\n', ' '))
    except Exception as e:
        print(f"{method} {url} -> ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    endpoints = [
        ("GET", "/signup", {}),
        ("GET", "/signin", {}),
        ("GET", "/profile", {}),
        ("POST", "/api/register", {"json": {"user": "name", "pass": "123", "mail": "email@example.com"}}),
        ("POST", "/api/login", {"json": {"user": "name", "pass": "123"}}),
    ]
    for method, url, kwargs in endpoints:
        hit(method, url, **kwargs)

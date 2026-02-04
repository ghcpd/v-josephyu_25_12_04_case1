from models import get_connection, User


def test_register_and_login_flow(app, client):
    # Register a new user
    resp = client.post(
        "/register",
        data={"username": "alice", "email": "alice@example.com", "password": "secret123"},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert resp.headers["Location"].endswith("/dashboard")

    # Verify the user exists in the DB
    conn = get_connection(app)
    user = User.get_by_username(conn, "alice")
    conn.close()
    assert user is not None
    assert user.email == "alice@example.com"
    assert user.verify_password("secret123")

    # Access dashboard as logged-in user (session should be set by registration)
    dash_resp = client.get("/dashboard")
    assert dash_resp.status_code == 200
    assert b"alice" in dash_resp.data


def test_login_with_wrong_password(app, client):
    # Seed a user
    conn = get_connection(app)
    User.create(conn, "bob", "correcthorsebattery", "bob@example.com")
    conn.close()

    # Attempt login with wrong password
    resp = client.post(
        "/login",
        data={"username": "bob", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Invalid username or password" in resp.data


def test_unique_username_and_email(app, client):
    # First registration
    resp1 = client.post(
        "/register",
        data={"username": "charlie", "email": "charlie@example.com", "password": "secret123"},
        follow_redirects=True,
    )
    assert resp1.status_code == 200

    # Duplicate username
    resp2 = client.post(
        "/register",
        data={"username": "charlie", "email": "other@example.com", "password": "secret123"},
        follow_redirects=True,
    )
    assert b"Username is already taken" in resp2.data

    # Duplicate email
    resp3 = client.post(
        "/register",
        data={"username": "otheruser", "email": "charlie@example.com", "password": "secret123"},
        follow_redirects=True,
    )
    assert b"Email is already registered" in resp3.data


def test_password_min_length_validation(app, client):
    resp = client.post(
        "/register",
        data={"username": "dana", "email": "dana@example.com", "password": "123"},
        follow_redirects=True,
    )
    assert b"Field must be between 6 and 128 characters long" in resp.data


def test_email_required_validation(app, client):
    resp = client.post(
        "/register",
        data={"username": "erin", "email": "", "password": "secret123"},
        follow_redirects=True,
    )
    # WTForms adds a generic "This field is required." message for missing email
    assert b"This field is required" in resp.data


def test_logout_requires_login(app, client):
    # Trigger login by registering
    client.post(
        "/register",
        data={"username": "frank", "email": "frank@example.com", "password": "secret123"},
        follow_redirects=True,
    )
    # Logout
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    # After logout, dashboard should redirect to login
    dash_resp = client.get("/dashboard", follow_redirects=False)
    assert dash_resp.status_code in (302, 303)
    location = dash_resp.headers["Location"]
    assert "/login" in location  # login redirect includes next param

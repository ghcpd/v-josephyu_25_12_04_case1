from models import get_connection, User


def test_user_crud(app):
    conn = get_connection(app)
    user = User.create(conn, "george", "mypassword", "george@example.com")
    assert user.id is not None

    fetched = User.get_by_username(conn, "george")
    assert fetched is not None
    assert fetched.id == user.id
    assert fetched.verify_password("mypassword")
    assert not fetched.verify_password("wrong")

    fetched_by_id = User.get_by_id(conn, user.id)
    assert fetched_by_id.username == "george"
    conn.close()

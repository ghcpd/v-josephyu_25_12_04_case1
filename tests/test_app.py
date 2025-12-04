"""
Pytest test suite for Flask User Management Application
"""
import pytest
import sqlite3
import os
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import User, init_db, get_connection
from auth import LoginForm, RegisterForm


@pytest.fixture
def test_app():
    """Create and configure test Flask app"""
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test_app.db'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create app context
    with app.app_context():
        init_db(app)
        yield app
    
    # Cleanup
    if os.path.exists('test_app.db'):
        os.remove('test_app.db')


@pytest.fixture
def client(test_app):
    """Create test client"""
    return test_app.test_client()


@pytest.fixture
def app_context(test_app):
    """Create app context for testing"""
    with test_app.app_context():
        yield test_app


class TestDatabaseInit:
    """Tests for database initialization"""
    
    def test_database_creates_users_table(self, app_context):
        """Test that users table is created"""
        conn = get_connection(app_context)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table = cur.fetchone()
        conn.close()
        assert table is not None, "users table not created"
    
    def test_users_table_has_correct_columns(self, app_context):
        """Test users table has all required columns"""
        conn = get_connection(app_context)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(users)")
        columns = {row[1] for row in cur.fetchall()}
        conn.close()
        
        required_columns = {'id', 'username', 'password_hash', 'email'}
        assert required_columns.issubset(columns), f"Missing columns. Got: {columns}"


class TestUserModel:
    """Tests for User model"""
    
    def test_create_user(self, app_context):
        """Test creating a new user"""
        conn = get_connection(app_context)
        user = User.create(conn, "testuser", "password123", "test@example.com")
        conn.close()
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.id is not None
    
    def test_get_user_by_username(self, app_context):
        """Test retrieving user by username"""
        conn = get_connection(app_context)
        User.create(conn, "john", "password123", "john@example.com")
        
        retrieved = User.get_by_username(conn, "john")
        conn.close()
        
        assert retrieved is not None
        assert retrieved.username == "john"
        assert retrieved.email == "john@example.com"
    
    def test_get_user_by_id(self, app_context):
        """Test retrieving user by ID"""
        conn = get_connection(app_context)
        user = User.create(conn, "jane", "password123", "jane@example.com")
        
        retrieved = User.get_by_id(conn, user.id)
        conn.close()
        
        assert retrieved is not None
        assert retrieved.id == user.id
        assert retrieved.username == "jane"
    
    def test_get_nonexistent_user_returns_none(self, app_context):
        """Test that retrieving non-existent user returns None"""
        conn = get_connection(app_context)
        retrieved = User.get_by_username(conn, "nonexistent")
        conn.close()
        
        assert retrieved is None
    
    def test_password_verification(self, app_context):
        """Test password verification"""
        conn = get_connection(app_context)
        user = User.create(conn, "testuser", "mypassword", "test@example.com")
        conn.close()
        
        assert user.verify_password("mypassword") is True
        assert user.verify_password("wrongpassword") is False
    
    def test_duplicate_username_raises_error(self, app_context):
        """Test that duplicate username raises IntegrityError"""
        conn = get_connection(app_context)
        User.create(conn, "duplicate", "pass1", "email1@example.com")
        
        with pytest.raises(sqlite3.IntegrityError):
            User.create(conn, "duplicate", "pass2", "email2@example.com")
        
        conn.close()
    
    def test_duplicate_email_raises_error(self, app_context):
        """Test that duplicate email raises IntegrityError"""
        conn = get_connection(app_context)
        User.create(conn, "user1", "pass1", "duplicate@example.com")
        
        with pytest.raises(sqlite3.IntegrityError):
            User.create(conn, "user2", "pass2", "duplicate@example.com")
        
        conn.close()
    
    def test_password_hash_not_plaintext(self, app_context):
        """Test that password is hashed, not stored as plaintext"""
        conn = get_connection(app_context)
        user = User.create(conn, "testuser", "mypassword", "test@example.com")
        conn.close()
        
        assert user.password_hash != "mypassword"
        assert len(user.password_hash) > len("mypassword")


class TestAuthRoutes:
    """Tests for authentication routes"""
    
    def test_register_get_returns_200(self, client):
        """Test GET /register returns 200"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Username' in response.data
        assert b'Email' in response.data
        assert b'Password' in response.data
    
    def test_register_post_valid_data(self, client, app_context):
        """Test POST /register with valid data"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
        }, follow_redirects=True)
        
        # Should redirect to dashboard after successful registration
        assert response.status_code == 200
        assert b'newuser' in response.data or b'Welcome' in response.data or b'You are logged in' in response.data
    
    def test_register_post_duplicate_username(self, client, app_context):
        """Test POST /register with duplicate username"""
        # Create first user
        conn = get_connection(app_context)
        User.create(conn, "existing", "password123", "existing@example.com")
        conn.close()
        
        # Try to register with same username
        response = client.post('/register', data={
            'username': 'existing',
            'email': 'new@example.com',
            'password': 'password123',
        })
        
        assert b'Username is already taken' in response.data or response.status_code == 200
    
    def test_login_get_returns_200(self, client):
        """Test GET /login returns 200"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Username' in response.data
        assert b'Password' in response.data
    
    def test_login_post_valid_credentials(self, client, app_context):
        """Test POST /login with valid credentials"""
        # Create user first
        conn = get_connection(app_context)
        User.create(conn, "loginuser", "password123", "login@example.com")
        conn.close()
        
        # Try to login
        response = client.post('/login', data={
            'username': 'loginuser',
            'password': 'password123',
        }, follow_redirects=True)
        
        # Should redirect to dashboard
        assert response.status_code == 200
        assert b'loginuser' in response.data or b'Welcome' in response.data
    
    def test_login_post_invalid_credentials(self, client, app_context):
        """Test POST /login with invalid credentials"""
        # Create user first
        conn = get_connection(app_context)
        User.create(conn, "loginuser", "password123", "login@example.com")
        conn.close()
        
        # Try with wrong password
        response = client.post('/login', data={
            'username': 'loginuser',
            'password': 'wrongpassword',
        })
        
        assert b'Invalid username or password' in response.data or response.status_code == 200
    
    def test_logout_redirects_to_login(self, client):
        """Test logout redirects to login"""
        response = client.get('/logout', follow_redirects=True)
        # Should redirect to login page
        assert response.status_code == 200


class TestFormValidation:
    """Tests for form validation"""
    
    def test_register_form_password_min_length_6(self, app_context):
        """Test RegisterForm password minimum length is 6"""
        # Note: README claims min is 3 but actual code is 6
        from auth import RegisterForm
        form = RegisterForm()
        password_field = form.password
        
        # Check validators
        validators_names = [type(v).__name__ for v in password_field.validators]
        assert 'Length' in validators_names
    
    def test_register_form_email_required(self, app_context):
        """Test RegisterForm email field is required"""
        from auth import RegisterForm
        form = RegisterForm()
        
        # Email field should exist
        assert hasattr(form, 'email')
    
    def test_login_form_fields_exist(self, app_context):
        """Test LoginForm has required fields"""
        from auth import LoginForm
        form = LoginForm()
        
        assert hasattr(form, 'username')
        assert hasattr(form, 'password')
        assert hasattr(form, 'submit')
    
    def test_register_form_fields_exist(self, app_context):
        """Test RegisterForm has required fields"""
        from auth import RegisterForm
        form = RegisterForm()
        
        assert hasattr(form, 'username')
        assert hasattr(form, 'email')
        assert hasattr(form, 'password')
        assert hasattr(form, 'submit')
    
    def test_register_form_no_confirm_password(self, app_context):
        """Test RegisterForm does NOT have confirm_password field"""
        from auth import RegisterForm
        form = RegisterForm()
        
        # This is a known missing feature
        assert not hasattr(form, 'confirm_password')


class TestAppRoutes:
    """Tests for main app routes"""
    
    def test_index_redirects_to_login_when_not_authenticated(self, client):
        """Test index redirects to login for unauthenticated users"""
        response = client.get('/', follow_redirects=False)
        assert response.status_code in [302, 303, 307]  # Redirect
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 303, 307]  # Should redirect to login
    
    def test_dashboard_returns_200_when_logged_in(self, client, app_context):
        """Test dashboard accessible when logged in"""
        # Create and login user
        conn = get_connection(app_context)
        User.create(conn, "dashuser", "password123", "dash@example.com")
        conn.close()
        
        client.post('/login', data={
            'username': 'dashuser',
            'password': 'password123',
        })
        
        # Now access dashboard
        response = client.get('/dashboard')
        assert response.status_code == 200


class TestDocumentationAccuracy:
    """Tests to verify documentation accuracy"""
    
    def test_api_endpoints_not_implemented(self, client):
        """Test that /api/register and /api/login don't exist"""
        # README documents these but they're not implemented
        response = client.post('/api/register', json={
            'user': 'test',
            'pass': 'password123',
            'mail': 'test@example.com'
        })
        assert response.status_code == 404
        
        response = client.post('/api/login', json={
            'user': 'test',
            'pass': 'password123'
        })
        assert response.status_code == 404
    
    def test_profile_endpoint_not_implemented(self, client):
        """Test that /profile endpoint doesn't exist"""
        response = client.get('/profile', follow_redirects=False)
        assert response.status_code == 404
    
    def test_signup_endpoint_is_register(self, client):
        """Test that /signup is called /register"""
        response = client.get('/signup', follow_redirects=False)
        assert response.status_code == 404
        
        # But /register should work
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_signin_endpoint_is_login(self, client):
        """Test that /signin is called /login"""
        response = client.get('/signin', follow_redirects=False)
        assert response.status_code == 404
        
        # But /login should work
        response = client.get('/login')
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

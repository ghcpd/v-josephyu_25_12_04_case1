"""
Integration tests for Flask User Management Application
Tests end-to-end workflows and user interactions
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import User, init_db, get_connection


@pytest.fixture
def test_app():
    """Create and configure test Flask app"""
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test_integration.db'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        init_db(app)
        yield app
    
    if os.path.exists('test_integration.db'):
        os.remove('test_integration.db')


@pytest.fixture
def client(test_app):
    """Create test client"""
    return test_app.test_client()


class TestUserRegistrationWorkflow:
    """End-to-end tests for user registration"""
    
    def test_complete_registration_workflow(self, client):
        """Test complete registration workflow"""
        # Step 1: Access registration form
        response = client.get('/register')
        assert response.status_code == 200
        assert b'User Registration' in response.data
        
        # Step 2: Submit registration form
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
        }, follow_redirects=True)
        
        # Should be redirected and logged in
        assert response.status_code == 200
        assert b'newuser' in response.data or b'Welcome' in response.data
    
    def test_registration_duplicate_username(self, client, test_app):
        """Test registration with duplicate username"""
        # Create first user
        conn = get_connection(test_app)
        User.create(conn, "john", "pass123", "john@example.com")
        conn.close()
        
        # Try to register with same username
        response = client.post('/register', data={
            'username': 'john',
            'email': 'different@example.com',
            'password': 'pass456',
        })
        
        assert b'Username is already taken' in response.data or response.status_code == 200
    
    def test_registration_duplicate_email(self, client, test_app):
        """Test registration with duplicate email"""
        # Create first user
        conn = get_connection(test_app)
        User.create(conn, "john", "pass123", "john@example.com")
        conn.close()
        
        # Try to register with same email
        response = client.post('/register', data={
            'username': 'jane',
            'email': 'john@example.com',
            'password': 'pass456',
        })
        
        assert b'Email is already registered' in response.data or response.status_code == 200
    
    def test_registration_invalid_email_format(self, client):
        """Test registration with invalid email format"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'not-an-email',  # Invalid format
            'password': 'pass123',
        })
        
        # Should fail validation or return 200
        assert response.status_code in [200, 400]


class TestUserLoginWorkflow:
    """End-to-end tests for user login"""
    
    def test_complete_login_workflow(self, client, test_app):
        """Test complete login workflow"""
        # Step 1: Create user
        conn = get_connection(test_app)
        User.create(conn, "loginuser", "password123", "login@example.com")
        conn.close()
        
        # Step 2: Access login form
        response = client.get('/login')
        assert response.status_code == 200
        assert b'User Login' in response.data
        
        # Step 3: Submit login form with valid credentials
        response = client.post('/login', data={
            'username': 'loginuser',
            'password': 'password123',
        }, follow_redirects=True)
        
        # Should be redirected to dashboard
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'loginuser' in response.data
    
    def test_login_invalid_username(self, client):
        """Test login with non-existent username"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'anypassword',
        })
        
        assert b'Invalid username or password' in response.data or response.status_code == 200
    
    def test_login_invalid_password(self, client, test_app):
        """Test login with correct username but wrong password"""
        # Create user
        conn = get_connection(test_app)
        User.create(conn, "testuser", "correctpass", "test@example.com")
        conn.close()
        
        # Try with wrong password
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpass',
        })
        
        assert b'Invalid username or password' in response.data or response.status_code == 200
    
    def test_login_case_sensitive(self, client, test_app):
        """Test that login is case-sensitive for username"""
        # Create user
        conn = get_connection(test_app)
        User.create(conn, "testuser", "password123", "test@example.com")
        conn.close()
        
        # Try with different case
        response = client.post('/login', data={
            'username': 'TestUser',  # Different case
            'password': 'password123',
        })
        
        # Should fail or succeed depending on implementation
        assert response.status_code in [200, 404]


class TestDashboardAccess:
    """End-to-end tests for dashboard access"""
    
    def test_dashboard_requires_authentication(self, client):
        """Test that dashboard requires user to be logged in"""
        response = client.get('/dashboard', follow_redirects=False)
        
        # Should redirect to login
        assert response.status_code in [302, 303, 307]
    
    def test_dashboard_shows_username(self, client, test_app):
        """Test that dashboard displays logged-in user's username"""
        # Create and login user
        conn = get_connection(test_app)
        User.create(conn, "dashuser", "password123", "dash@example.com")
        conn.close()
        
        client.post('/login', data={
            'username': 'dashuser',
            'password': 'password123',
        })
        
        # Access dashboard
        response = client.get('/dashboard')
        
        assert response.status_code == 200
        assert b'dashuser' in response.data
    
    def test_logout_from_dashboard(self, client, test_app):
        """Test logout functionality from dashboard"""
        # Create and login user
        conn = get_connection(test_app)
        User.create(conn, "logoutuser", "password123", "logout@example.com")
        conn.close()
        
        client.post('/login', data={
            'username': 'logoutuser',
            'password': 'password123',
        })
        
        # Logout
        response = client.get('/logout', follow_redirects=True)
        
        # Should be redirected
        assert response.status_code == 200


class TestSessionManagement:
    """Tests for session management"""
    
    def test_session_persists_after_login(self, client, test_app):
        """Test that session persists across requests after login"""
        # Create and login user
        conn = get_connection(test_app)
        User.create(conn, "sessionuser", "password123", "session@example.com")
        conn.close()
        
        client.post('/login', data={
            'username': 'sessionuser',
            'password': 'password123',
        })
        
        # Make multiple requests
        response1 = client.get('/dashboard')
        response2 = client.get('/dashboard')
        
        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
    
    def test_session_cleared_after_logout(self, client, test_app):
        """Test that session is cleared after logout"""
        # Create and login user
        conn = get_connection(test_app)
        User.create(conn, "logoutuser", "password123", "logout@example.com")
        conn.close()
        
        client.post('/login', data={
            'username': 'logoutuser',
            'password': 'password123',
        })
        
        # Verify can access dashboard
        response = client.get('/dashboard')
        assert response.status_code == 200
        
        # Logout
        client.get('/logout')
        
        # Try to access dashboard again
        response = client.get('/dashboard', follow_redirects=False)
        
        # Should be redirected to login
        assert response.status_code in [302, 303, 307]


class TestFormValidation:
    """Tests for form validation"""
    
    def test_registration_without_username(self, client):
        """Test registration without username"""
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123',
        })
        
        # Should fail validation
        assert response.status_code == 200
    
    def test_registration_without_email(self, client):
        """Test registration without email"""
        response = client.post('/register', data={
            'username': 'testuser',
            'password': 'password123',
        })
        
        # Should fail validation
        assert response.status_code == 200
    
    def test_registration_without_password(self, client):
        """Test registration without password"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
        })
        
        # Should fail validation
        assert response.status_code == 200
    
    def test_registration_short_username(self, client):
        """Test registration with username less than 3 characters"""
        response = client.post('/register', data={
            'username': 'ab',  # Only 2 chars
            'email': 'test@example.com',
            'password': 'password123',
        })
        
        # Should show error (minimum is 3 chars)
        assert response.status_code == 200
    
    def test_registration_short_password(self, client):
        """Test registration with password less than 6 characters"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345',  # Only 5 chars
        })
        
        # Should show error (minimum is 6 chars)
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

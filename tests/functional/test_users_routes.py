from musicblog.models import User


# ==================== REGISTRATION TESTS ====================


def test_register_page_loads(test_client, init_database):
    """Test registration page loads"""
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_user_registration(test_client, register_user):
    """Test user can register"""
    response = register_user

    assert response.status_code == 200
    assert b'Your account has been created! You are now able to log in!' in response.data
    assert len(response.history) == 1
    assert response.request.path == "/login"
    
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.username == 'newuser'
    assert user.email == 'test@example.com'

def test_user_authenticated(test_client, login_user):
    """Test that logged-in users are redirected from login page"""

    response = test_client.get('/register', follow_redirects=True)

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/home"

def test_user_registration_with_existing_email(test_client, register_user):
    """Test user registration fails with existing email"""

    response = test_client.post('/register', 
        data={
            'username': 'newuser1',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=True
    )

    assert b'That email is taken. Please choose another.' in response.data
    assert b'Register' in response.data

def test_user_registration_with_existing_username(test_client, register_user):
    """Test user registration fails with existing username"""

    response = test_client.post('/register', 
        data={
            'username': 'newuser',
            'email': 'newtest@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=True
    )

    assert b'That username is taken. Please choose another.' in response.data
    assert b'Register' in response.data

def test_user_registration_pw_mismatch(test_client, init_database):
    """Test user confirm password mismatch"""
    response = test_client.post('/register', 
        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password321'
        },
        follow_redirects=True
    )

    assert b'Field must be equal to password.' in response.data
    user = User.query.filter_by(email='new@example.com').first()
    assert user is None


# ==================== LOGIN TESTS ====================


def test_login_page_loads(test_client, init_database):
    """Test registration page loads"""
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_user_login(test_client, login_user):
    """Test user can login"""
    response = login_user

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/home"

def test_login_with_remember_me(test_client, register_user):
    """Test login with remember me checked"""
    response = test_client.post('/login',
        data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember': True
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert response.request.path == "/home"

def test_login_with_wrong_email(test_client, register_user):
    """Test login with incorrect email"""
    response = test_client.post('/login',
        data={
            'email': 'new@example.com',
            'password': 'testpassword123'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Login Unsuccessful. Please check username and password' in response.data
    assert response.request.path == "/login"

def test_login_with_wrong_pw(test_client, register_user):
    """Test login with incorrect password"""
    response = test_client.post('/login',
        data={
            'email': 'test@example.com',
            'password': 'testpassword'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Login Unsuccessful. Please check username and password' in response.data
    assert response.request.path == "/login"

def test_login_redirects_to_next_page(test_client, register_user):
    """Test that login redirects to 'next' parameter if provided"""
    # Try to access protected page (account)
    response = test_client.get('/account')
    
    # Should redirect to login with next parameter
    assert response.status_code == 302
    assert '/login' in response.location
    
    # Login with next parameter
    response = test_client.post('/login?next=/account',
        data={
            'email': 'test@example.com',
            'password': 'password123'
        },
        follow_redirects=True
    )
    
    # Should be on account page now
    assert response.status_code == 200
    assert b'Account' in response.data
    assert response.request.path == "/account"

def test_user_autheticated(test_client, login_user):
    """Test that logged-in users are redirected from login page"""
    response = test_client.get('/login', follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/home"


# ==================== LOGOUT TESTS ====================


def test_logout(test_client, login_user):
    """Test user can logout"""
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Home' in response.data
    assert response.request.path == "/home"


# ==================== ACCOUNT TESTS ====================


def test_account_page_requires_login(test_client, init_database):
    """Test that account page redirects to login if not authenticated"""
    response = test_client.get('/account')
    
    assert response.status_code == 302
    assert '/login' in response.location

def test_account_page_loads(test_client, login_user):
    """Test that account page loads for logged-in user"""
    response = test_client.get('/account')
    
    assert response.status_code == 200
    assert b'Account' in response.data

    assert b'newuser' in response.data
    assert b'test@example.com' in response.data

def test_account_update_username_email(test_client, login_user):
    """Test updating username and email on account page"""
    response = test_client.post('/account',
        data={
            'username': 'updateduser',
            'email': 'newtest@example.com'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Your account has been updated!' in response.data

    user = User.query.filter_by(email='newtest@example.com').first()
    assert user.username == 'updateduser'
    assert user.email == 'newtest@example.com'

def test_account_update_username(test_client, login_user):
    """Test updating username on account page"""
    response = test_client.post('/account',
        data={
            'username': 'updateduser',
            'email': 'test@example.com'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Your account has been updated!' in response.data

    user = User.query.filter_by(email='test@example.com').first()
    assert user.username == 'updateduser'
    assert user.email == 'test@example.com'

def test_account_taken_username(test_client, register_users):
    """Test account update fails when trying to use existing username"""
    test_client.post('/login',
        data={
            'email': 'test1@example.com',
            'password': 'password123'
        },
        follow_redirects=True
    )

    response = test_client.post('/account',
        data={
            'username': 'newuser2',
            'email': 'test1@example.com'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'That username is taken. Please choose another.' in response.data

    user = User.query.filter_by(email='test1@example.com').first()
    assert user.username == 'newuser1'
    assert user.email == 'test1@example.com'

def test_account_taken_email(test_client, register_users):
    """Test account update fails when trying to use existing email"""
    test_client.post('/login',
        data={
            'email': 'test1@example.com',
            'password': 'password123'
        },
        follow_redirects=True
    )

    response = test_client.post('/account',
        data={
            'username': 'newuser1',
            'email': 'test2@example.com'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'That email is taken. Please choose another.' in response.data

    user = User.query.filter_by(email='test1@example.com').first()
    assert user.username == 'newuser1'
    assert user.email == 'test1@example.com'
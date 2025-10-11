from musicblog.models import User
 
# ==================== REGISTRATION TESTS ====================

def test_register_page_loads(test_client):
    """Test registration page loads"""
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_user_registration(test_client, init_database):
    """Test user can register"""
    response = test_client.post('/register', 
        data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Your account has been created! You are now able to log in!' in response.data
    assert len(response.history) == 1
    assert response.request.path == "/login"
    
    user = User.query.filter_by(email='new@example.com').first()
    assert user is not None
    assert user.username == 'newuser'
    assert user.email == 'new@example.com'

def test_user_registration_with_existing_email(test_client):
    """Test user registration fails with existing email"""
    response = test_client.post('/register', 
        data={
            'username': 'newuser1',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'That email is taken. Please choose another.' in response.data
    assert b'Register' in response.data

def test_user_registration_with_existing_username(test_client):
    """Test user registration fails with existing email"""
    response = test_client.post('/register', 
        data={
            'username': 'newuser',
            'email': 'newtest@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'That username is taken. Please choose another.' in response.data
    assert b'Register' in response.data

def test_user_authenticated(test_client):
    """Test user can register"""
    test_client.post('/login', 
        data={
            'email': 'new@example.com',
            'password': 'password123',
        },
        follow_redirects=True
    )

    response = test_client.get('/register', follow_redirects=True)

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/home"
    
    



    


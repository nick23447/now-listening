import pytest
from musicblog import create_app, db
from musicblog.config import TestConfig
from functional.test_data import UserFactory, PostFactory

registration_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

@pytest.fixture(scope='module')
def test_app():
    """Create application for testing - created once per test file"""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
   
@pytest.fixture(scope='module')
def test_client(test_app):
    """Create a test client - created once per test file"""
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    """Reset database before each test - fresh start for every test function"""
    with test_app.app_context():
        # Clean up any existing data
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        yield db
        
        # Clean up after test
        db.session.remove()

@pytest.fixture(scope='function')
def register_user(test_client, init_database):
    """Register user through HTTP"""
    response = test_client.post('/register', 
        data=registration_data,
        follow_redirects=True
    )

    return response

@pytest.fixture(scope='function')
def login_user(test_client, register_user):
    """Provide a logged-in client"""
    response = test_client.post('/login', 
        data=login_data,
        follow_redirects=True
    )

    return response

@pytest.fixture(scope='function')
def test_user(init_database):
    """Create test user"""
    user = UserFactory.create()
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='function')
def test_users(init_database):
    """Create 3 test users"""
    users = UserFactory.create_batch(3)
    for user in users:
        db.session.add(user)

    db.session.commit()
    return users

@pytest.fixture(scope='function')
def sample_post(test_user):
    """Create post"""
    post = PostFactory.create(author=test_user)
    db.session.add(post)
    db.session.commit()
    return post
    
@pytest.fixture(scope='function')
def sample_posts(test_users):
    """Create 3 posts"""
    posts = PostFactory.create_batch(3, test_users)
    for post in posts:
        db.session.add(post)
    db.session.commit()
    return posts


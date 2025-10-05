import pytest
from musicblog import create_app, db
from musicblog.config import TestConfig
from functional.test_data import UserFactory, PostFactory

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
def test_users(init_database, amount):
    """Create test user/s"""
    if amount == 1:
        user = PostFactory.create()
        db.session.add(user)
        db.session.commit()
        return user
   
    users = PostFactory.create_batch()
    for user in users:
        db.session.add(user)

    db.session.commit()
    return users

@pytest.fixture(scope='function')
def sample_posts(test_app, test_users):
   ...

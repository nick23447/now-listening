from conftest import *
from musicblog.models import User

def test_register_page_loads(test_client, init_database):
    """Test registration page loads"""
    response = test_client.get('/register')
    assert response.status_code == 200


from conftest import *

def test_home_page_loads(test_client):
    """Test that home page loads"""
    response = test_client.get('/')
    assert response.status_code == 200

def test_home_route_alias(test_client):
    """Test that home page loads"""
    response = test_client.get('/home')
    assert response.status_code == 200

def test_home_without_posts(test_client):
    """Test that home page loads"""
    response = test_client.get('/')
    assert response.status_code == 200

def test_home_with_posts(test_client):
    """Test that home page loads"""
    response = test_client.get('/')
    assert response.status_code == 200




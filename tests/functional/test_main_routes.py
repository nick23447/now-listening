from musicblog.models import User, Post

# ==================== Home TESTS ====================   

def test_home_route(test_client):
    """Test that home page loads"""
    response = test_client.get('/')
    assert response.status_code == 200
 
def test_home_route_alias(test_client):
    """Test that home page loads"""
    response = test_client.get('/home')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_home_with_posts(test_client, sample_posts):
    """Test that posts load"""
    response = test_client.get('/home')
    html = response.data.decode('utf-8')

    assert len(Post.query.all()) 

    assert response.status_code == 200
    assert 'Test Post 1' in html
    assert 'Test Post 2' in html
    assert 'Test Post 3' in html

def test_posts_ordered(test_client, sample_posts):
    """Test that posts are ordered by date (newest first)"""
    response = test_client.get('/home')
    html = response.data.decode('utf-8')
    
    assert response.status_code == 200
    
    # Find position of each post title
    post1_pos = html.find('Test Post 1')  # Newest
    post2_pos = html.find('Test Post 2')  # Middle
    post3_pos = html.find('Test Post 3')  # Oldest

    assert len(Post.query.all()) == 3
    
    # All should exist
    assert post1_pos != -1
    assert post2_pos != -1
    assert post3_pos != -1
    
    # Newest (Post 1) should appear first
    assert post1_pos < post2_pos < post3_pos, \
        f"Posts in wrong order. Found at positions: Post1={post1_pos}, Post2={post2_pos}, Post3={post3_pos}"




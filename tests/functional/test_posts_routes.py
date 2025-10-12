from musicblog.models import Post


# ==================== SEARCH ALBUM TESTS ====================


def test_search_album(test_client):
    """Test that home page loads"""
    response = test_client.get('/search_album')
    assert response.status_code == 200


# ==================== NEW POST TESTS ====================


def test_new_post(test_client):
    """Test that home page loads"""
    response = test_client.get("/post/new", follow_redirects=True)
    assert response.status_code == 200



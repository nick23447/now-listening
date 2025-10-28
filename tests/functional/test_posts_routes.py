from musicblog.models import Post
from unittest.mock import patch


# ==================== SEARCH ALBUM TESTS ====================


def test_search_album_loads(test_client):
    """Test that home page loads"""
    response = test_client.get('/search_album')
    assert response.status_code == 200

def test_search_album_query(test_client):
    mock_token = 'fake_token'

    mock_response = {
        "albums": {
            "items": [{"name": "Test Album", "artists": [{"name": "Test Artist"}]}]
        }
    }

    with patch("musicblog.posts.routes.get_spotify_token", return_value=mock_token), \
         patch("musicblog.posts.routes.requests.get") as mock_get:

        mock_get.return_value.json.return_value = mock_response

        res = test_client.get("/search_album?q=test")

        assert res.status_code == 200
        data = res.get_json()
        assert "albums" in data
        assert data["albums"]["items"][0]["name"] == "Test Album"

   

# ==================== NEW POST TESTS ====================


def test_new_post(test_client):
    """Test that home page loads"""
    response = test_client.get("/post/new", follow_redirects=True)
    assert response.status_code == 200



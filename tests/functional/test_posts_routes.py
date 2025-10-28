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


def test_new_post_get(login_user, test_client):
    """GET /post/new should render form when logged in"""
    response = test_client.get("/post/new")
    assert response.status_code == 200
    assert b'New Post' in response.data
    assert b'<form' in response.data

def test_new_post_post(login_user, test_client, init_database):
    """POST /post/new should create a post"""
    post_data = {
        'title': 'My Album Review',
        'content': 'Great album!',
        'album_name': 'The Test Album',
        'album_artist': 'Mock Artist',
        'album_image': 'https://i.scdn.co/image/ab67616d0000b2736a760642a56847027428cb61'
    }

    response = test_client.post(
        "/post/new",
        data=post_data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Your post has been created!' in response.data

    post = Post.query.first()
    assert post is not None
    assert post.title == "My Album Review"
    assert post.author is not None
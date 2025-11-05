from musicblog.models import Album


def check_if_album_exists(album_name: str, album_artist: str) -> bool:
	album_in_ratings = Album.query.filter_by(name=album_name, artist=album_artist).first()
	return True if album_in_ratings else False

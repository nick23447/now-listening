import os
import requests
from typing import Optional, Union, cast
from werkzeug.wrappers import Response
from flask import render_template, url_for, flash, redirect, Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from musicblog import db
from musicblog.models import Post, Album, AlbumRating, User
from musicblog.posts.forms import PostForm
from sqlalchemy import func

posts = Blueprint('posts', __name__)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# ---------- Spotify API ----------
def get_spotify_token() -> Optional[str]:
	auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    )
	token =  auth_response.json().get("access_token")
	assert isinstance(token, str), "Spotify token missing or not a string"
	return token

@posts.route('/search_album')
def search_album() -> Response:
	query = request.args.get("q", "").strip()
	if not query:
		return cast(Response, jsonify({"albums": {"items":[]}}))
	
	token = get_spotify_token()   
	limit = request.args.get("limit", 20)
	headers = {"Authorization": f"Bearer {token}"} 

	res = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=album&limit={limit}",
        headers=headers
    )
    
	return cast(Response, jsonify(res.json()))


# ---------- New Post ----------
@posts.route('/post/new', methods=['GET','POST'])
@login_required #type: ignore
def new_post() -> Union[str, Response]:
	form = PostForm()
	if form.validate_on_submit():

		album = Album.query.filter_by(
            name=form.album_name.data.strip(),
            artist=form.album_artist.data.strip()
        ).first()
		
		if not album:
			album = Album(
                name=form.album_name.data.strip(),
                artist=form.album_artist.data.strip(),
                image=form.album_image.data
            )
			db.session.add(album)
			db.session.flush()
		
		existing_rating = AlbumRating.query.filter_by(
			user_id=current_user.id,
			album_id=album.id
		).first()
		
		if existing_rating:
			existing_rating.rating = form.rating.data

		else:
			album_rating = AlbumRating(
				user_id=current_user.id,
				album_id=album.id,
				rating=form.rating.data
			)
			db.session.add(album_rating)

		post = Post(
			title=form.title.data, 
			content=form.content.data, 
			rating=form.rating.data,
			album_name=form.album_name.data, 
			album_artist=form.album_artist.data,
			album_image=form.album_image.data, 
			album_id=album.id,
			author=current_user
		)

	
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', 
		title='New Post', 
		form=form,
		legend='Create Post')


# ---------- Individual Posts ----------
@posts.route("/post/<int:post_id>")
def post(post_id: int) -> str:
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


# ---------- Update Post ----------
@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required #type: ignore
def update_post(post_id: int) -> Union[str, Response]:
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)

	album_name = Album.query.filter_by(
		name=post.album_name, 
		artist=post.album_artist
	).first()
	
	album_rating = AlbumRating.query.filter_by(
		user_id=current_user.id,
		album_id=album_name.id
	).first()

	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		post.rating = form.rating.data
		post.album_name=form.album_name.data
		post.album_artist=form.album_artist.data
		post.album_image=form.album_image.data
		post.author=current_user
		album_rating.rating = form.rating.data

		db.session.commit()
		flash('Your post had been updated!', 'success')
		return redirect(url_for('posts.post', post_id=post_id))
	
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		form.rating.data = post.rating

	return render_template('create_post.html', 
		title='Update Post', 
		form=form,
		legend='Update Post')


# ---------- Delete Post ----------
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required #type: ignore
def delete_post(post_id: int) -> Response:
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	
	album = Album.query.filter_by(name=post.album_name).first()
	album_rating = AlbumRating.query.filter_by(album_id=album.id).first()

	db.session.delete(post)
	db.session.delete(album)
	db.session.delete(album_rating)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))


# ---------- Average Ratings ----------
@posts.route("/album_ratings")
def album_ratings() -> str:
    page = request.args.get('page', 1, type=int)
    albums_with_avg_ratings = (
        db.session.query(
            Album.id,
            Album.name,
            Album.artist,
            Album.image,
            func.avg(AlbumRating.rating).label('average_rating'),
            func.count(AlbumRating.id).label('rating_count')
        )
        .outerjoin(AlbumRating, Album.id == AlbumRating.album_id)
        .group_by(Album.id)
        .order_by(func.avg(AlbumRating.rating).desc())
        .paginate(page=page, per_page=12)
    )
    return render_template('album_ratings.html', title='Album Ratings', albums=albums_with_avg_ratings)


@posts.route("/album/<int:album_id>")
def album_detail(album_id: int) -> str:
    album = Album.query.get_or_404(album_id)

    posts = Post.query.filter_by(album_id=album.id).order_by(Post.date_posted.desc()).all()
    ratings = (
        db.session.query(User.username, AlbumRating.rating)
        .join(User, User.id == AlbumRating.user_id)
        .filter(AlbumRating.album_id == album.id)
        .all()
    )

    avg_rating = album.avg_rating
    rating_count = album.total_ratings

    return render_template(
        "album_detail.html",
        title=f"{album.name} by {album.artist}",
        album=album,
        posts=posts,
        ratings=ratings,
        avg_rating=avg_rating,
		rating_count=rating_count
    )

import os
import requests
from flask import render_template, url_for, flash, redirect, Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from musicblog import db
from musicblog.models import Post
from musicblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
	auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    )
	return auth_response.json().get("access_token")


@posts.route('/search_album')
def search_album():
	query = request.args.get("q", "").strip()
	if not query:
		return jsonify({"albums": {"items":[]}}) 
	
	token = get_spotify_token()   
	limit = request.args.get("limit", 20)
	headers = {"Authorization": f"Bearer {token}"} 

	res = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=album&limit={limit}",
        headers=headers
    )
    
	return jsonify(res.json())

@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(
			title=form.title.data, 
			content=form.content.data, 
			album_name=form.album_name.data, 
			album_artist=form.album_artist.data,
			album_image=form.album_image.data, 
			author=current_user)
		
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', 
		title='New Post', 
		form=form,
		legend='Create Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		post.album_name=form.album_name.data
		post.album_artist=form.album_artist.data
		post.album_image=form.album_image.data
		post.author=current_user
		db.session.commit()
		flash('Your post had been updated!', 'success')
		return redirect(url_for('posts.post', post_id=post_id))
	
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('create_post.html', 
		title='Update Post', 
		form=form,
		legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

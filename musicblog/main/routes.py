from flask import render_template, Blueprint, request
from musicblog.models import Post, User
from typing import cast
from sqlalchemy.orm import InstrumentedAttribute

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home() -> str:
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(
		cast(InstrumentedAttribute, Post.date_posted).desc()
		).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)

@main.route('/user/<string:username>')
def user_posts(username: str) -> str:
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
		.order_by(
		cast(InstrumentedAttribute, Post.date_posted).desc())\
		.paginate(page=page, per_page=5)
	
	return render_template('user_posts.html', posts=posts, user=user)


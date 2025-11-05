from flask import render_template, Blueprint, request, flash, url_for, redirect
from markupsafe import Markup
from musicblog.models import Post, User
from typing import cast, Union
from werkzeug.wrappers import Response
from sqlalchemy.orm import InstrumentedAttribute
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/about')
def about() -> str:
	return render_template('about.html')


@main.route('/home')
def home() -> str:
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(
		cast(InstrumentedAttribute, Post.date_posted).desc()
		).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)


@main.route('/user/<string:username>')
def user_posts(username: str) -> Union[str, Response]:
	user = User.query.filter_by(username=username).first()
	
	if not user:
		flash(
            Markup(
                'You need to <a href="' + url_for('users.login') +
                '" class="alert-link">log in</a> or <a href="' +
                url_for('users.register') +
                '" class="alert-link">create an account</a> to view user posts.'
            ),
            'warning'
        )
		return redirect(url_for('users.login'))  

	page = request.args.get('page', 1, type=int)

	posts = Post.query.filter_by(author=user)\
		.order_by(
		cast(InstrumentedAttribute, Post.date_posted).desc())\
		.paginate(page=page, per_page=5)
	
	return render_template('user_posts.html', posts=posts, user=user)


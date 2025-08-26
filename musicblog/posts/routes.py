from flask import render_template, url_for, flash, redirect, Blueprint
from musicblog import db
from musicblog.models import Post
from musicblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('home.html'))
	return render_template('create_post.html', title='New Post', form=form)
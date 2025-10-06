from flask import render_template, Blueprint
from musicblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	posts = Post.query.order_by(Post.date_posted.desc())
	return render_template('home.html', posts=posts)



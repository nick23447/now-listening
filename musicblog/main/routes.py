from flask import render_template, Blueprint
from musicblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)



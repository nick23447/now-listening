from flask import render_template, Blueprint, request
from musicblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)


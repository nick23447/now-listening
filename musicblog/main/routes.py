from flask import Blueprint

main = Blueprint('main', __name__)




main.route('/')
main.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)



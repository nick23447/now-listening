from musicblog import app
from flask import render_template, url_for


posts = [
     {
          'author': 'John Doe',
          'title': 'Music Post 1',
          'content': 'First post content',
          'date_posted': 'April 20, 2018'

     },
     {
          'author': 'Jane Doe',
          'title': 'Music Post 2',
          'content': 'Second post content',
          'date_posted': 'April 21, 2018'
     }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

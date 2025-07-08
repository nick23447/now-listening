from musicblog import app
from flask import render_template, url_for, flash, redirect
from musicblog.forms import RegistrationForm, LoginForm


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


@app.route('/register')
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    return render_template('login.html')

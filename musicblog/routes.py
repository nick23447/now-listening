from flask import render_template, url_for, flash, redirect
from musicblog import app, db, bcrypt
from musicblog.forms import RegistrationForm, LoginForm
from musicblog.models import User, Post
from flask_login import login_user, current_user


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


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_autheticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in!", 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
          user = User.query.filter_by(email=form.email.data).first()
          if user and bcrypt.check_password_hash(user.password, form.password.data):
              login_user(user, remember=form.remember.data)
              return redirect(url_for('home'))

          flash('Login Unsuccessful. Please check username and password', 'danger')
     
    return render_template('login.html', title='Login', form=form)


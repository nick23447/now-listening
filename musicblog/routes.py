from flask import render_template, url_for, flash, redirect
from musicblog import app
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


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
          flash('You have been logged in!', 'success')
          return redirect(url_for('home'))
        
        flash('Login Unsuccessful. Please check username and password', 'danger')
     
    return render_template('login.html', title='Login', form=form)


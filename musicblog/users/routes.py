import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from musicblog import db, bcrypt
from musicblog.models import User
from musicblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from musicblog.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
    
	form = RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f"Your account has been created! You are now able to log in!", 'success')
		return redirect(url_for('users.login'))
    
	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
    
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))

		flash('Login Unsuccessful. Please check username and password', 'danger')
     
	return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			old_pic = current_user.image_file
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
			if old_pic != 'default.jpg':
				os.remove(os.path.join(current_app.root_path, 'static/profile_pics', old_pic))
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
		
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	
	form = RequestResetForm()
	return render_template('users.reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	
	user = User.verify_reset_token(token)
	if not user:
		flash('That is an invalid or expired token', "warning")
		return redirect(url_for('users.reset_request'))
	
	form = ResetPasswordForm()
	return render_template('users.reset_token.html', title='Reset Password', form=form)

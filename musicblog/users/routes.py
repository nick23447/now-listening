from __future__ import annotations
import os
from typing import Union, Optional
from flask import (
    render_template, 
    url_for, 
    flash, 
    redirect, 
    request, 
    Blueprint, 
    current_app,
)
from werkzeug.wrappers import Response
from flask_login import login_user, current_user, logout_user, login_required
from musicblog import db, bcrypt, mail
from musicblog.models import User
from musicblog.users.forms import(
	RegistrationForm, 
	LoginForm, 
	UpdateAccountForm, 
	RequestResetForm, 
	ResetPasswordForm
)
from musicblog.users.utils import save_picture
from musicblog.users.utils import send_reset_email

users = Blueprint('users', __name__)


# ---------- REGISTER ----------
@users.route('/register', methods=['GET','POST'])
def register() -> Union[str, Response]:
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


# ---------- Login ----------
@users.route('/login', methods=['GET','POST'])
def login() -> Union[str, Response]:
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
    
	form = LoginForm()

	if form.validate_on_submit():
		user: User = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))

		flash('Login Unsuccessful. Please check username and password', 'danger')
     
	return render_template('login.html', title='Login', form=form)


# ---------- LOGOUT ----------
@users.route('/logout')
def logout() -> Response:
	logout_user()
	return redirect(url_for('main.home'))


# ---------- ACCOUNT ----------
@users.route('/account', methods=['GET','POST'])
@login_required # type: ignore 
def account() -> Union[str, Response]:
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			old_pic = current_user.image_file
			picture_file: str = save_picture(form.picture.data)
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


# ---------- RESET REQUEST ----------
@users.route("/reset_password", methods=['GET','POST'])
def reset_request() -> Union[str, Response]:
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	
	return render_template('reset_request.html', title='Reset Password', form=form)


# ---------- RESET TOKEN ----------
@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token: str) -> Union[str, Response]:
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	user: Optional[User] = User.verify_reset_token(token)

	if not user:
		flash('That is an invalid or expired token', "warning")
		return redirect(url_for('users.reset_request'))
	
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f"Your password has been updated! You are now able to log in.", 'success')
		return redirect(url_for('users.login'))
	
	return render_template('reset_token.html', title='Reset Password', form=form)

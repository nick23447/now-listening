import os
import secrets
from typing import cast
from PIL import Image
from flask import current_app, url_for
from wtforms.fields import Field
from musicblog.models import User
from musicblog import mail

from flask_mail import Message

def save_picture(form_picture: Field) -> str:
	random_hex: str = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn: str = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	form_picture.save(picture_path)
	
	# outpute_size = (125,125)
	# i = Image.open(form_picture)
	# i.thumbnail(outpute_size)
	# i.save(picture_path)
	
	return picture_fn

def send_reset_email(user: User) -> None:
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and  no changes will be made.
"""
	mail.send(msg)
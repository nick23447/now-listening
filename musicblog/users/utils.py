import os
import secrets
from PIL import Image
from musicblog import app

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	form_picture.save(picture_path)

	# outpute_size = (125,125)
	# i = Image.open(form_picture)
	# i.thumbnail(outpute_size)
	# i.save(picture_path)
	
	return picture_fn
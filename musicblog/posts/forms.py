from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    album_name = HiddenField('Album Name', validators=[DataRequired()])
    album_artist = HiddenField('Album Artist', validators=[DataRequired()])
    album_image = HiddenField('Album Image', validators=[DataRequired()])
    submit = SubmitField('Post')

    
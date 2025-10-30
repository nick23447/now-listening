from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=1000)])
    album_name = HiddenField('Album Name', validators=[DataRequired(message="Please select an album from the search.")])
    album_artist = HiddenField('Album Artist', validators=[DataRequired()])
    album_image = HiddenField('Album Image', validators=[DataRequired()])
    submit = SubmitField('Post')

    
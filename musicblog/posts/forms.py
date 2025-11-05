from __future__ import annotations
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    HiddenField, 
    IntegerField
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    NumberRange
)

class PostForm(FlaskForm): # type: ignore
    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=1000)])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5, message="Rating must be between 1 and 5")])
    album_name = HiddenField('Album Name', validators=[DataRequired(message="Please select an album from the search.")])
    album_artist = HiddenField('Album Artist', validators=[DataRequired()])
    album_image = HiddenField('Album Image', validators=[DataRequired()])
    submit = SubmitField('Post')

    
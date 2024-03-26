from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, StringField
from wtforms.validators import ValidationError, DataRequired, Optional, Length


class updateBio(FlaskForm):
    name = StringField("Display name", validators=[Optional(), Length(max=100)])
    location = StringField("Your location", validators=[Optional(), Length(max=100)])
    interests = StringField("Tell the world about your interests", validators=[Optional()])
    bio = TextAreaField("A brief summary about you", validators=[Optional()])


class aboutForm(FlaskForm):
    about = TextAreaField("Give a brief professional summary about you", validators=[DataRequired()])

class fileForm(FlaskForm):
    file = FileField("Choose file", validators=[DataRequired()])
    
    

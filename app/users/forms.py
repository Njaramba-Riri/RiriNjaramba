from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField
from wtforms.validators import ValidationError, DataRequired


class fileForm(FlaskForm):
    file = FileField("Choose file", validators=[DataRequired()])
    
    
class aboutForm(FlaskForm):
    about = TextAreaField("Give a brief professional summary about you", validators=[DataRequired()])

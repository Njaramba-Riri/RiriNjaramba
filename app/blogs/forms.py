from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, Optional, Length

class CommentForm(FlaskForm):
    """Defines the form rendered on blog page for user comments.

    Args:
        Form:Base dorm class. 
    """
    email = StringField("Your Email:", validators=[Optional(), Email()])
    name = StringField("Your Name:", validators=[DataRequired(message="Name field can't be empty"), 
                                                 Length(max=30)])
    comment = TextAreaField("Your Comment:", validators=[DataRequired(message="Comment field can't be null ffs."), 
                                                       Length(max=500, message="Comment can't be more than 500 characters.")])
    captcha = RecaptchaField()
    submit = SubmitField("comment")
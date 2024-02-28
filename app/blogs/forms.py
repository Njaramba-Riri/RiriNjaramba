from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import Email, DataRequired, Optional, Length
from flask_pagedown.fields import PageDownField

class BlogPost(FlaskForm):
    title = PageDownField("Blog title", validators=[DataRequired(message="Jameni, this field can't be empty.")])
    body = PageDownField("Your blog content", validators=[DataRequired()])
    submit = SubmitField("Publish")

class CommentForm(FlaskForm):
    """Defines the form rendered on blog page for user comments.

    Args:
        Form:Base dorm class. 
    """
    email = StringField("Your Email:", validators=[DataRequired(), Email()])
    name = StringField("Your Name:", validators=[DataRequired(message="Name field can't be empty"), 
                                                 Length(max=30)])
    mawoni = TextAreaField("Your Comment:", validators=[DataRequired(message="Comment field can't be null ffs."), 
                                                       Length(max=500, message="Comment can't be more than 500 characters.")])
    #captcha = RecaptchaField(validators=[DataRequired(message="This is a required field.")])
    submit = SubmitField("comment")


class replyCommentForm(FlaskForm):
    """Defines form for user repplies to other comments.

    Args:
        FlaskForm (Form): Base form class.
    """
    reply = TextAreaField("Type your reply...", validators=[DataRequired(), Length(max=200, message="Replies shouldn't be that long jameni. Eiyyy.")])
    comment_id = HiddenField("Comment ID", validators=[DataRequired()])
    submit = SubmitField("Reply.")

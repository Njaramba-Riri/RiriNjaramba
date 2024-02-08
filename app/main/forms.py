from flask_wtf import FlaskForm
from wtforms import StringField ,TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email

class FeedbackForm(FlaskForm):
    email = StringField("Your Email Address.", validators=[DataRequired(), 
                                                          Email(message='Kindly enter a valid email address.')])
    feed = TextAreaField("What services are you looking for?.", validators=[DataRequired(message="You can't submit empty message."), 
                                                                      InputRequired(), Length(min=10, max=200)])
    submit = SubmitField("Enquire")
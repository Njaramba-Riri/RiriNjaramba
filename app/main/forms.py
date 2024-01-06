from flask_wtf import Form
from wtforms import StringField ,TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email

class FeedbackForm(Form):
    email = StringField("Your Email Address.", validators=[DataRequired(), 
                                                          Email(message='Kindly enter a valid email address.')])
    feed = TextAreaField("Ask or enquire about anything.", validators=[DataRequired(message="You can't submit empty message."), 
                                                                      InputRequired(), Length(min=10, max=200)])
    submit = SubmitField("Submit")
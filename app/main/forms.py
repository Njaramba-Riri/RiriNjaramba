from flask_wtf import FlaskForm
from wtforms import StringField ,TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, Email

class FeedbackForm(FlaskForm):
    email = StringField("Your Email Address.", validators=[DataRequired(), 
                                                          Email(message='Kindly enter a valid email address.')])
    feed = TextAreaField("What services are you looking for?.", validators=[DataRequired(message="You can't submit empty message."), 
                                                                      InputRequired(), Length(min=10, max=200)])
    submit = SubmitField("Enquire")
    
class quoteForm(FlaskForm):
    name = StringField("Your name.", validators=[DataRequired()])
    email = StringField("Your email address.", validators=[DataRequired(),
                                                          Email(message="Enter a valid email address.")])
    services = SelectField("What service are you looking for?.", 
                           choices=[('', "---Click to Select One---"), 
                                    ("Machine Learning Model", "ML Model"),
                                    ("MLOps", "MLOps"), ("Experiment Tracking", "Experiment Tracking"),
                                    ("Model Deployment", "Model Deployment"),
                                    ("Consultation", "IT Consultation"), ("IT Support", "IT Support"),
                                    ("Web Application", "Web Application")], validators=[DataRequired()])
    more = TextAreaField("Tell me more about it.", validators=[DataRequired(),
                                                              Length(min=10, max=1000)])

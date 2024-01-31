import re

from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError

from .models import User

class LoginForm(FlaskForm):
    """Creates user login form.

    Args:
        Form (_type_): Base class for all flask forms.
    """
    email = StringField("Enter Email: ", validators=[Email(), DataRequired()])
    username = StringField("Enter username: ", validators=[DataRequired()])
    password = PasswordField("Enter Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember Me", validators=[Optional()])
    login = SubmitField("Login")

    def validate(self, extra_validators=None):
        check_validate = super(LoginForm, self).validate(extra_validators)
        if not check_validate:
            return False
        user  = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("User with such username doesn't exist.")
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append("Wrong password, try again.")
            return False
        return True 
    
class RegisterForm(FlaskForm):
    """Creates user register form.

    Args:
        Form: An instance of flask form.
    """
    email = StringField('Enter Email.', validators=[DataRequired(), Email()])
    username = StringField('Enter Preferred Username.', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password. ', validators=[DataRequired(), Length(min=8) ])
    confirm = PasswordField('Confirm Password. ', validators=[DataRequired(), EqualTo('password', 
                                                                                      message="Both password and confirm password fields must match.")])
    #recaptcha = RecaptchaField()
    register = SubmitField("Register")
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("A user with that email already exists.")
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is already in use, try another.")
        
class forgotPass(FlaskForm):
    """Create a forgotten password form.

    Args:
        FlaskForm (any): Flask form.
    """
    email = StringField("Kindly enter your email.", validators=[DataRequired(), 
                                                                Email(message="Weka valid email address bana.")])

    def validate_email(self, field):
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
        #     raise ValidationError("Enter a valid email address.")
        
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("User with such an email address doesn't exist yet.")
        
class resetPassword(FlaskForm):
    """Create a password reset form fields.

    Args:
        FlaskForm (Any): Flask form instance.
    """
    password = PasswordField("New Password.", validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField("Confirm new password.", validators=[DataRequired(),
                                                                 EqualTo('password', message="Both passoword fields must match.")])
    submit = SubmitField("Send")
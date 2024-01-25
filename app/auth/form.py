from flask_wtf import Form
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

from .models import User

class LoginForm(Form):
    """Creates user login form.

    Args:
        Form (_type_): Base class for all flask forms.
    """
    email = StringField("Enter Email: ", validators=[Email(), DataRequired()])
    usename = StringField("Enter username: ", validators=[DataRequired()])
    password = PasswordField("Enter Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember Me", validators=[Optional()])
    login = SubmitField("Login")

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False
        user  = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("User with such username doesn't exist.")
            return False
        if not self.user.check_password(self.password.data):
            self.password.errors.append("Wrong password, try again.")
            return False
        return True 
    
class RegisterForm(Form):
    """Creates user register form.

    Args:
        Form: An instance of flask form.
    """
    email = StringField('Enter Email: ', validators=[DataRequired(), Email()])
    username = StringField('Enter Username', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=8) ])
    confirm = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    
    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("User with that name already exists")
            return False
        return True
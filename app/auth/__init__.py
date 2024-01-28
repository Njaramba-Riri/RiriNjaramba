from flask_login import LoginManager, AnonymousUserMixin
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
login = LoginManager()
mail = Mail()
jwt = JWTManager()

login.login_view = 'auth.signin'
login.login_message = "Kindly login to access this page."
login.session_protection = "strong"
login.login_message_category = "info"


@login.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.get(user_id)

class VisitorAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = "Ariff"

def create_app(app, **kwargs):
    """Creates and registers authentication blueprint int the main app.

    Args:
        app (Any): An instance of flask app.
    """
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
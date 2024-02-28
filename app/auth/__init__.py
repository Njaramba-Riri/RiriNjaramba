from functools import wraps

from flask import abort
from flask_login import LoginManager, AnonymousUserMixin, login_manager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_login import current_user

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
    return User.query.get(user_id)

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        super().__init__()
        self.username = "Ariff"
        self.email = "anonymoususer@gmail.com"
   
    def gravatar(self, size):
        return False
    
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    from .models import Permission
    return permission_required(Permission.ADMINISTER)(f)

def create_app(app, **kwargs):
    """Creates and registers authentication blueprint into the main app.

    Args:
        app (Any): An instance of flask app.
    """
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

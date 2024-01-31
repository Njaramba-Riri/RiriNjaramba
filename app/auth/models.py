from datetime import datetime, timedelta, timezone
from time import time
import jwt

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin

from app import db
from . import bcrypt

class User(UserMixin, db.Model):
    """Creates the user object db model in the data base.

    Args:
        db (_type_): Base class for all models.
    """
    __tablename__ = "Users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean(), default=False)
    created = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password) 
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

    def generate_confirmation_token(self, expiration=3000):
        """Generates a confirmation token when  user creates account.

        Args:
            expiration (int, optional): How long should the token stay `alive` before espiring. Defaults to 3000.

        Returns:
            : confirmation token.
        """
        confirm_token = jwt.encode(
            {
                "confirm_id": self.id,
                "expiration": (datetime.now(tz=timezone.utc) +
                                timedelta(seconds=expiration)).isoformat()
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return confirm_token
    
    def confirm_token(self, token):
        """Verifies the authenticity of the just generated token.

        Args:
            token (bytes): Confirmation token to be confirmed. 

        Returns:
            Bool: True if the token passes confirmation test, else False.
        """
        try:
            token_data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime(seconds=2000).fromisoformat(),
                algorithms=['HS256']
            )
        except:
            return False
        if token.data.get('confirm_id') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_pass_reset_token(self, expiration=3600):
        """Genererates a password reset token in the instance of user not remembering his/her password.

        Args:
            expiration (int, optional): The time the token takes to expire. Defaults to 3600.

        Returns:
            Bytes: The confirmation token.
        """
        token = jwt.encode(
            {
                "reset_id": self.id,
                "expiration": time() + expiration
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'            
        )

    @staticmethod
    def confirm_reset_token(token, new_password):
        """Verifies the confirmation token genarated by the password reset func.

        Args:
            new_password(Str): The new password set by the user..

        Returns:
            Bool: True if the token passes verification test, else False. 
        """
        try:
            token_data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_id']
        except:
            return False
        user = db.session.get(User, token_data)
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    def ping(self):
        """Pings the user object.

        Returns:
            _type_: _description_
        """
        self.last_seen = datetime.now(datetime.timezone.utc)
        db.session.add(self)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
        
    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    @property    
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)
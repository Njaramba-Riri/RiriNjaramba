import datetime
from time import time
import hashlib

import jwt
from flask import current_app, request, has_request_context
from flask_login import AnonymousUserMixin, UserMixin

from app import db
from config import Permission
from . import bcrypt

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean(), default=False, index=True)
    permissions = db.Column(db.Integer())
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles  = {
            'User': (Permission.COMMENT |
                     Permission.WRITE_ARTICLE, True),
            'Moderator': (Permission.COMMENT |
                          Permission.MODERATE_COMMENTS |
                          Permission.WRITE_ARTICLE, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

        

    def __repr__(self) -> str:
        return 'Role: {}'.format(self.name)


class User(UserMixin, db.Model):
    """Creates the user object db model in the data base.

    Args:
        db (_type_): Base class for all models.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(100))
    bio = db.Column(db.String(500))
    about = db.Column(db.Text())
    interests = db.Column(db.String(500))
    location = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean(), default=False)
    avatar_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    created = db.Column(db.DateTime(), default=datetime.datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.now)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    comments = db.relationship('Comments', backref='author', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["ADMIN"]:
                self.confirmed = True
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')
            ).hexdigest()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password) 
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if has_request_context() and request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating 
        )
    
    def generate_confirmation_token(self, expiration=3600):
        """Generates a confirmation token when  user creates account.

        Args:
            expiration (int, optional): How long should the token stay `alive` before espiring. Defaults to 3000.

        Returns:
            : confirmation token.
        """
        token = jwt.encode(
            {
                "confirm_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm  ="HS256"
        )
        return token
    
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
                leeway = datetime(seconds=20),
                algorithms = ["HS256"]
            )
        except:
            return False
        if token_data.get('confirm_id') != self.id:
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
        self.last_seen = datetime.datetime.utcnow()
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
    
    def get_id(self):
        UnicodeDecodeError
        return str(self.id)
    
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(permissions=Permission.ADMINISTER)

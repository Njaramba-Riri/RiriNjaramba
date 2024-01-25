from datetime import datetime, timezone
from flask_login import AnonymousUserMixin
import unicodedata

from app import db
from . import bcrypt

class User(db.Model):
    """Creates the user object db model in the data base.

    Args:
        db (_type_): Base class for all models.
    """
    __tablename__ = "Users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    def set_password(self, password):
        return bcrypt.generate_password_hash(self.password, password) 
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
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
        return unicodedata(self.id)
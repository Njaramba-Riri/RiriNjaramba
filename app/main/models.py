import os
import datetime
from app import db

class Feedback(db.Model):
    __tablename__ = 'Feedback'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    feed = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, email, feed):
        self.email = email
        self.feed = feed

    def __repr__(self):
        return f"Feedback(id={self.id}, email='{self.email}', feed='{self.feed}')"
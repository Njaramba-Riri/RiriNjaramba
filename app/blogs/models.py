from datetime import datetime, timezone

from app import db


tags = db.Table(
    "blog tags",
    db.Column('post_id', db.Integer(), db.ForeignKey('Blogs.post_id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)

class Posts(db.Model):
    """Represents the posts that are stred in the database.

    Args:
        db (_type_): Base class for all db models.
    """
    __tablename__="Blogs"

    post_id = db.Column(db.Integer(), primary_key=True)
    post_author = db.Column(db.String(100), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False, unique=True, index=True)
    post = db.Column(db.Text(), nullable=False)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('Blogs', lazy='dynamic'))
    comment = db.relationship('Comments', backref='Blogs', lazy='dynamic')
    updated = db.Column(db.Boolean(), default=False, nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime(), default=datetime.now(timezone.utc), 
                             onupdate=datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return "<author: {}>".format(self.post_author) 


class Tag(db.Model):
    """Represents the post tags.

    Args:
        db (sa.Model): Base class for all models.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        return f"<name: {self.name}>"
    

class Comments(db.Model):
    """Blog posts comments database model.

    Args:
        db (sa.Model): Base class for all db models.
    """
    __tablename__ = "Blog Comments"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    comment = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    blog_id = db.Column(db.Integer(), db.ForeignKey('Blogs.post_id'))

    def __str__(self) -> str:
        return "<comment: {}>".format(self.comment[:15])
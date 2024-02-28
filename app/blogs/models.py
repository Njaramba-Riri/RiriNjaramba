from datetime import datetime, timezone

from markdown import markdown
import bleach

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
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String(100), nullable=False, unique=True, index=True)
    title_html = db.Column(db.Text()) 
    post = db.Column(db.Text(), nullable=False)
    post_html = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('Blogs', lazy='dynamic'))
    comments = db.relationship('Comments', backref='blog', lazy='dynamic')
    updated = db.Column(db.Boolean(), default=False, nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime(), default=datetime.now(timezone.utc), 
                             onupdate=datetime.now(timezone.utc))
    
    @staticmethod
    def on_changed_body(target, value, oldvalue,initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'ul', 'pre', 'strong', 'h1',
            'h2', 'h3', 'p'
        ]

        target.title_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='xhtml'),
            tags=allowed_tags, strip=True
        ))
        target.post_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='xhtml'),
            tags=allowed_tags, strip=True
        ))


    def __repr__(self) -> str:
        return "<author: {}>".format(self.post_author) 

db.event.listen(Posts.post, 'set', Posts.on_changed_body)

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
    comment_html = db.Column(db.Text())
    disabled = db.Column(db.Boolean())
    blog_id = db.Column(db.Integer(), db.ForeignKey('Blogs.post_id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))    
    date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    @staticmethod
    def on_changed_body(value, target, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'strong'
        ]

        target.comment_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))


    def __repr__(self) -> str:
        return "<comment: {}>".format(self.comment[:15])
    
db.event.listen(Comments.comment, 'set', Comments.on_changed_body)

class CommentReply(db.Model):
    """Comments replies db representation.

    Args:
        db (SQLALCHEMY): Base class for all db models. 
    """
    __tablename__ = "comment_reply"

    reply_id = db.Column(db.Integer(), primary_key=True)
    reply = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    comment_id = db.Column(db.Integer(), db.ForeignKey('Blog Comments.id'))

    def __repr__(self):
        return '<Reply: {}'.format(self.reply)

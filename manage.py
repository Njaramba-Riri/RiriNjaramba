import os

from app import db, migrate, create_app

from app.auth.models import Role, User
from app.main.models import Feedback, Quotes
from app.blogs.models import Posts, Comments, Tag, CommentReply

env = os.environ.get("APP_ENV", 'dev')
app = create_app('config.%sConfig' % env.capitalize())

@app.shell_context_processor
def make_shell_context():
    return dict(application=app, database=db, 
                quotes=Quotes,feed_model=Feedback, users=User, 
                posts_model=Posts, comments=Comments, replies=CommentReply, 
                post_tags=Tag, roles=Role, db_migrate=migrate)

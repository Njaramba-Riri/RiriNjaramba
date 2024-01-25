import os

from app import db, migrate, create_app
from app.main.models import Feedback
from app.blogs.models import Posts

env = os.environ.get("RIRI_ENV", 'dev')
app = create_app('config.%sConfig' % env.capitalize())

@app.shell_context_processor
def make_shell_context():
    return dict(application=app, database=db, feed_model=Feedback, posts_model=Posts, db_migrate=migrate)
import logging
import random

from faker import Faker

from app import db
from app.blogs.models import Posts, Tag, Comments
from app.main.models import Feedback

logging.basicConfig(format=("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
fake = Faker()
Faker.seed(123)

def generate_tag(n: int):
    """Generates blog post tags.

    Args:
        n (int): Number of tags to generate.

    Returns:
        db.Model: Instance of base class, a database model.
    """
    tags = list()
    for i in range(n):
        log.info("Generating tags...")
        tag = Tag()
        tag.name = fake.color_name()
        
        try:
            log.info("Adding tags to db...")
            db.session.add(tag)
            db.session.commit()
            tags.append(tag)
        except Exception as e:
            log.error("Error when adding tag %s: %s" %(str(tag), e))
            db.session.rollback()
    return tags  

def generate_comment(n: int) -> db.Model:
    """Generates blog posts comments.

    Args:
        n (int): Number of comments to generate.

    Returns:
        db.Model: Instance of sqlalchemy database model.
    """
    comments = list()
    for _ in range(n):
        comment = Comments()

        comment.email = fake.email()
        comment.name = fake.name()
        comment.comment = fake.text()
        comment.date = fake.date_this_decade(before_today=True, after_today=False)
        #comment.post_id = post[random.randrange(0, len(post))].post_id

        try:
            db.session.add(comment)
            db.session.commit()
            comments.append(comment)
        except Exception as e:
            log.error("Couldn't add comment `%s`: %s" %(str(comment), e))
            db.session.rollback()
    return comments

def generate_blogs(n: int, tags: list, comments: list) -> db.Model:
    """Generates fake blog posts.

    Args:
        n (int): Number of fake blogs to be generated.

    Returns:
        db.Model: An instance of sqlalchemy database model.
    """
    posts = list()
    for _ in range(n):
        post = Posts()

        post.post_author = "Riri Njaramba"
        post.title = fake.sentence()
        post.post = fake.text(max_nb_chars=2000)
        #post.tags = [tags[random.randrange(0, 10)] for i in range(0, 2)]
        #post.comment = comments[random.randrange(0, 30)].comment
        post.updated = fake.boolean()
        post.date_created = fake.date_this_decade(before_today=True, after_today=False)
        post.date_updated = fake.date_this_decade(before_today=True, after_today=False)

        try:
            db.session.add(post)
            db.session.commit()
            posts.append(post)
        except Exception as e:
            log.error("Error while creating blog posts: {}".format(e))
            db.session.rollback()


def generate_feed(n: int) -> db.Model:
    """Generates fake feedback.

    Args:
        n (int): Number of fake feedback to be generated.

    Returns:
        db.Model: A feedback database model.

    Raises:
        Exception.
    """
    feedback = list()
    for i in range(n):
        feed = Feedback()

        feed.email = fake.email()
        feed.feed = fake.text()
        feed.created_at = fake.date_this_century(before_today=True, after_today=False)
        feed.updated_at = fake.date_this_century(before_today=True, after_today=False)

        try:
            db.session.add(feed)
            db.session.commit()
            feedback.append(feed)
        except Exception as e:
            log.error("Encountered error while generating feedback: {}".format(e))
            db.session.rollback()
            raise e
    return feedback
    
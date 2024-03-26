import os
import logging
import random
import hashlib

from faker import Faker

from app import db
from app.blogs.models import Posts, Tag, Comments, CommentReply
from app.main.models import Feedback
from app.auth.models import User

logging.basicConfig(format=("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
fake = Faker()
Faker.seed(123)


def generate_users(n: int):
    for i in range(n):
        user = User()
        
        user.email = fake.email()
        user.display_name = fake.name()
        user.username = str(user.display_name).split(None)[0]
        user.set_password("testing12")
        city = fake.city()
        country = fake.country()
        user.location = f'{city}, {country}'
        user.bio = fake.sentence()
        user.about = fake.text(max_nb_chars=2000)
        user.interests = random.choice(['Farming', 'Technology', 'Hunting', 'Bowling'])
        user.confirmed = random.choice([0, 1])
        user.role_id = random.choice([1, 2])
        user.avatar_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()
        user.created = fake.date_this_decade(before_today=True, after_today=False)
        user.last_seen = fake.date_this_year(before_today=True, after_today=False)
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

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

def generate_comment(n: int):
    """Generates blog posts comments.

    Args:
        n (int): Number of comments to generate.

    Returns:
        db.Model: Instance of sqlalchemy database model.
    """
    comments = list()
    for i in range(n):
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

def generate_comment_replies(n: int, comment: list):
    """Generates replies on the comments made to the blog. 

    Args:
        n (int): Number of replies to generate.

    Returns:
        db.Model: Replies db model. 
    """
    replies = list()
    for i in range(n):
        reply = CommentReply()

        reply.reply = fake.text()
        reply.date = fake.date_this_decade(before_today=True, after_today=False)
        #reply.comment_id = comment[random.randrange(0, len(comment))].comment.id

        try:
            db.session.add(reply)
            db.session.commit()
            replies.append(reply)
        except Exception as e:
            log.error("Fail to add reply %s: %s" % (str(reply), e))
            db.session.rollback()

    return replies



def generate_blogs(n: int, tags: list, comments: list):
    """Generates fake blog posts.

    Args:
        n (int): Number of fake blogs to be generated.

    Returns:
        db.Model: An instance of sqlalchemy database model.
    """
    posts = list()
    for i in range(n):
        post = Posts()

        post.post_author = "Riri Njaramba"
        post.title = fake.sentence()
        post.post = fake.text(max_nb_chars=5000)
        post.tags = [tags[random.randrange(0, 10)] for i in range(len(tags))]
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
    
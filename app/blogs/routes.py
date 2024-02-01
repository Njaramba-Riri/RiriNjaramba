import logging
import random

logging.basicConfig(format=("%(asctime)s: %(name)s:%(levelname)s: %(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, url_for, request, flash, redirect
from sqlalchemy import exc

from app import db
from .models import Posts, Comments, CommentReply, Tag
from .forms import CommentForm, replyCommentForm

blog_blueprint = Blueprint("blogs", __name__, static_folder="/blogs/static",
                           template_folder="/templates/blogs", url_prefix="/RiriNjaramba/blogs/")

@blog_blueprint.route('/', methods=['GET', 'POST'])
def blog_index():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_created.desc())
    blogs = db.paginate(posts, page=page, per_page=4, error_out=False)
    next_url = url_for('blogs.blog_index', page=blogs.next_num) if blogs.has_next else None
    prev_url = url_for('blogs.blog_index', page=blogs.prev_num) if blogs.has_prev else None
    tag = Tag.query.all()
    tags = random.sample(tag, 3)
    return render_template("blogs/index.html", posts=blogs.items,tags=tags,
                           next=next_url, prev=prev_url)
 
@blog_blueprint.route("/<string:title>", methods=["POST", "GET"])
def blog(title):
    post = Posts.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = Comments.query.filter_by(blog_id=post.post_id).order_by(Comments.date.desc())
    #comments = Comments.query.order_by(Comments.date.desc())
    # comment = random.sample(comments, 5)
    pagination = db.paginate(comments, page=page, per_page=5, error_out=False)
    next_url = url_for('blogs.blog', title=post.title, page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('blogs.blog', title=post.title, page=pagination.prev_num) if pagination.has_prev else None
    replies = CommentReply.query.all()
    form = CommentForm()
    reply_form = replyCommentForm()
    if form.validate_on_submit():
        comment = Comments()
        comment.email = form.email.data
        comment.name = form.name.data
        comment.comment = form.comment.data
        comment.blog_id = post.post_id
        try:
            db.session.add(comment)
            db.session.commit()
            flash("Your comment was submitted successfully.", category="info")
            return redirect(url_for('blogs.blog', title=title))
        except Exception as e:
            logger.info("Error while adding comment: {}".format(e))
            flash("Error: {}".format(e))
            db.session.rollback()
    if reply_form.validate_on_submit():
        reply = CommentReply(reply=reply_form.reply.data, comment_id=reply_form.comment_id.data)
        try:
            db.session.add(reply)
            db.session.commit()
            flash("Reply sent successfully", category="info")
            return redirect(url_for('blogs.blog', title=title))
        except exc.IntegrityError as e:
            logger.error("User reply could not be sent: {}".format(e))
            db.session.rollback()
    return render_template("blogs/blog.html", blog=post, 
                           form=form, reply=reply_form, replies=replies,
                           comments=pagination.items, next=next_url, prev=prev_url)
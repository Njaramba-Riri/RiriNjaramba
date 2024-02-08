import logging
import random

logging.basicConfig(format=("%(asctime)s: %(name)s:%(levelname)s: %(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, url_for, request, flash, redirect, session, abort, current_app
from flask_login import current_user
from sqlalchemy import exc

from app import db
from .models import Posts, Comments, CommentReply, Tag
from .forms import BlogPost, CommentForm, replyCommentForm
from ..auth import permission_required, admin_required 
from ..auth.models import Permission

blog_blueprint = Blueprint("blogs", __name__, static_folder="/blogs/static",
                           template_folder="/templates/blogs", url_prefix="/RiriNjaramba/blogs/")

@blog_blueprint.route('/', methods=['GET', 'POST'])
def blog_index():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_created.desc())
    blogs = db.paginate(posts, page=page, per_page=4, error_out=False)
    tag = Tag.query.all()
    tags = random.sample(tag, 3)
    return render_template("blogs/index.html", posts=posts,tags=tags, pagination=blogs,
                           permission=Permission)
 
@blog_blueprint.route("/<string:title>", methods=["POST", "GET"])
def blog(title):
    post = Posts.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = Comments.query.filter_by(blog_id=post.post_id).order_by(Comments.date.desc())
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
        comment.author = current_user._get_current_object()
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
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() -1) / current_app.config['COMMENTS_PER_PAGE'] + 1
        pagination  = post.comments.order_by(Comments.date.desc()).paginate(
            page=page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False
        )

        comments = pagination.items

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
                           form=form, reply=reply_form, replies=replies, comments=comments,
                           comment=pagination.items, next=next_url, prev=prev_url, permission=Permission)


@blog_blueprint.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return redirect(url_for('blogs.blog', title=post.title))

@blog_blueprint.route('/new', methods=['POST', 'GET'])
@permission_required(Permission.WRITE_ARTICLE)
def new_blog():
    blogs = Posts.query.order_by(Posts.date_created.desc())
    page = request.args.get('page')
    pagination = db.paginate(blogs, page=page, per_page=3, error_out=False)
    form = BlogPost()
    if current_user.can(Permission.WRITE_ARTICLE) and form.validate_on_submit():
        post = Posts(post_author=current_user.username, title=form.title.data, 
                     post=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.blog', title=post.title))
    return render_template("blogs/new_blog.html", form=form, permission=Permission, 
                           blogs=pagination.items, pagination=pagination ,title=session.get('title'))

@blog_blueprint.route("/edit/<string:title>", methods=['POST', 'GET'])
@permission_required(Permission.WRITE_ARTICLE)
def edit_blog(title):
    blog = Posts.query.filter_by(title=title).first()
    if current_user != blog.post_author \
        and not current_user.can(Permission.ADMINISTER):
        abort(404)
    posts = Posts.query.filter_by(author=blog.author)
    page = request.args.get('page')
    pagination = db.paginate(posts, page=page, per_page=3, error_out=False)
    form = BlogPost()
    if form.validate_on_submit():
        edited_blog = Posts(title=form.title.data, post=form.body.data) 
        try:
            db.session.add(edited_blog)
            # db.session.commit()
            session['title'] = edited_blog.title
            flash("BLog post has been updated, your're reading the latest version.", category="info")
            return redirect(url_for('.blog', title=edited_blog.title))
        except exc.IntegrityError as e:
            db.session.rollback()
            logger.error("Error when updating plog post: {}".format(e))
            flash("For some unforeseen reason, blog post could not be updated", category="warning")
    form.title.data = blog.title
    form.body.data = blog.post
    session['title'] = blog.title
    return render_template("blogs/new_blog.html", form=form, title=session.get('title'),
                            permission=Permission, pagination=pagination, user=blog.author)

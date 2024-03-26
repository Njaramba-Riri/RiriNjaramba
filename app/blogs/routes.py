import logging
import random

logging.basicConfig(format=("%(asctime)s: %(name)s:%(levelname)s: %(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, url_for, request, flash, redirect, session, abort, current_app
from flask_login import current_user, login_required
from sqlalchemy import exc, func, text

from app import db
from .models import Posts, Comments, CommentReply, Tag, tags
from .forms import BlogPost, CommentForm, replyCommentForm
from ..auth import permission_required, admin_required
from ..auth.models import Permission, User

blog_blueprint = Blueprint("blogs", __name__, static_folder="/blogs/static",
                           template_folder="/templates/blogs", url_prefix="/bytes")


def sidebar_data():
    recent = Posts.query.order_by(
        Posts.date_created.desc()
    ).limit(5).all()
    
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    
    return recent, top_tags
    

@blog_blueprint.route('/', methods=['GET', 'POST'])
def blog_index():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_created.desc())
    blogs = db.paginate(posts, page=page, per_page=4, error_out=False)
    # tag = Tag.query.all()
    # tags = random.sample(tag, 3)
    recent, top_tags = sidebar_data() 
    return render_template("blogs/index.html", posts=posts,
                           top=top_tags,
                           pagination=blogs, recent=recent,
                           permission=Permission)
 
@blog_blueprint.route("/<string:title>", methods=["POST", "GET"])
def blog(title):
    post = Posts.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = Comments.query.filter_by(blog_id=post.post_id).order_by(Comments.date.desc())
    pagination = db.paginate(comments, page=page, per_page=5, error_out=False)
    next_url = url_for('blogs.blog', title=post.title, page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('blogs.blog', title=post.title, page=pagination.prev_num) if pagination.has_prev else None
    replies = CommentReply.query.order_by(CommentReply.date.desc()).all()
        
    form = CommentForm()
    reply_form = replyCommentForm()
    
    if form.validate_on_submit():
        comment = Comments()
        comment.email = form.email.data
        comment.name = form.name.data
        comment.blog = post
        if current_user.is_authenticated: 
            comment.author = current_user._get_current_object()
        comment.comment = form.mawoni.data
        comment.blog_id = post.post_id
        try:
            db.session.add(comment)
            db.session.commit()
            flash("Your comment was submitted successfully.", category="info")
            return redirect(url_for('blogs.blog', title=title, page=-1))
        except Exception as e:
            db.session.rollback()
            logger.info("Error while adding comment: {}".format(e))
            flash("Error: {}".format(e), category="warning")
    page = request.args.get('page', 1, type=int)     
    if page == -1:
        page = (post.comments.count() -1) / current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination  = post.comments.order_by(Comments.date.asc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False
        )
    comments = pagination.items
            
    return render_template("blogs/blog.html", blog=post, 
                           form=form, reply=reply_form, replies=replies, 
                           comments=comments, pagionation=pagination, enumerate=enumerate,
                           comment=pagination.items, next=next_url, prev=prev_url, permission=Permission)

@blog_blueprint.route("/comment/<int:comment_id>/reply/", methods=['POST', 'GET'])
def comment_reply(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first_or_404()
    
    reply = CommentReply()
    reply_form = replyCommentForm()
    if request.method == 'POST' and reply_form.validate_on_submit():
        if current_user.is_authenticated:
            email = current_user.email 
            name = current_user.username
        else:
            email = reply_form.email.data
            name = reply_form.name.data    
        
        reply.email = email
        reply.name = name
        reply.reply = reply_form.reply.data
        reply.comment_id = comment.id
        try:
            db.session.add(reply)
            db.session.commit()
            flash("Reply sent successfully", category="info")
            return redirect(url_for('blogs.blog', title=comment.blog.title))
        except Exception as e:
            db.session.rollback()
            flash(f"Reply not sent: {e}", category="warning")
            logger.error("User reply could not be sent: {}".format(e))
    return redirect(url_for('blogs.blog', title=comment.blog.title))

@blog_blueprint.route("/tag/<string:tag_name>")
def blog_by_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    posts = tag.Blogs.order_by(Posts.date_created.desc()).all()
    
    recent, top_tags = sidebar_data()
    
    return render_template("blogs/tag.html", posts=posts, tag=tag_name,
                           recent=recent, top=top_tags, permission=Permission)

@blog_blueprint.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return redirect(url_for('blogs.blog', title=post.title))

@blog_blueprint.route('/new/', methods=['POST', 'GET'])
@login_required
@permission_required(Permission.WRITE_ARTICLE)
def new_blog():
    user = User.query.get_or_404(current_user.id)
    blogs = user.posts.order_by(Posts.date_created.desc()).limit(5).all()
    # page = request.args.get('page')
    # pagination = db.paginate(blogs, page=page, per_page=3, error_out=False)
    form = BlogPost()
    if current_user.can(Permission.WRITE_ARTICLE) and form.validate_on_submit():
        post = Posts(post_author=current_user.username, title=form.title.data, 
                     post=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.blog', title=post.title))
    return render_template("blogs/new_blog.html", form=form, permission=Permission, 
                           blogs=blogs, user=user)

@blog_blueprint.route("/edit/<int:blog_id>/", methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLE)
def edit_blog(blog_id):
    blog = Posts.query.filter_by(post_id=blog_id).first()
    user = User.query.filter_by(username=blog.author.username).first_or_404()
    if current_user != blog.post_author \
        and not current_user.can(Permission.ADMINISTER):
        abort(404)
    posts = user.posts.order_by(Posts.date_created.desc()).limit(5).all()
    form = BlogPost()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.post = form.body.data
        try:
            db.session.add(blog)
            db.session.commit()
            flash("BLog post has been updated, your're reading the latest version.", category="info")
            return redirect(url_for('.blog', title=blog.title))
        except exc.IntegrityError as e:
            db.session.rollback()
            logger.error("Error when updating plog post: {}".format(e))
            flash("For some unforeseen reason, blog post could not be updated", category="warning")
    form.title.data = blog.title
    form.body.data = blog.post
    return render_template("blogs/edit.html", form=form, posts=posts,
                            blog=blog, user=blog.author, permission=Permission)

@blog_blueprint.route('/remove/<int:blog_id>', methods=['DELETE', 'GET'])
@login_required
@permission_required(Permission.WRITE_ARTICLE)
def delete(blog_id):
    blog = Posts.query.filter_by(post_id=blog_id).first_or_404()
    try:
        db.session.delete(blog)
        db.session.commit()
        flash("Your blog piost has been deleted successfully.", category="info")
        return redirect(url_for(".blog_index", page=1))
    except Exception as e:
        db.session.rollback()
        flash("Your blog was not deleted, try later.", category="warning")
        return redirect(url_for('.blog_index', page=1))
        
@blog_blueprint.route("/hide/<int:blog_id>/", methods=['POST', 'GET'])
@login_required
@permission_required(Permission.WRITE_ARTICLE)
def hide(blog_id):
    blog = Posts.query.filter_by(post_id=blog_id).first_or_404()
    try:
        if blog.disabled:
            blog.disabled = False
        elif not blog.disabled:
            blog.disabled = True
        
        db.session.add(blog)
        db.session.commit()
        flash("Blog's visibility status updated successfully", category="info")
        return redirect(url_for('.blog_index', page=1))
    except Exception as e:
        db.session.rollback()
        flash("Blog visibility status not changed, try later", category="warning")
        return redirect(url_for('.blog_index', page=1))
        

@blog_blueprint.route("/moderate-comments/")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comments.query.order_by(Comments.date.desc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    
    return render_template("blogs/moderate.html", pagination=pagination,
                           comments=comments, page=page, permission=Permission)
    
@blog_blueprint.route("/comment/enable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comments.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@blog_blueprint.route("/comment/disable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comments.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@blog_blueprint.route("/comment/delete/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_delete(id):
    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!.", category='info')
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@blog_blueprint.route('/comments', methods=['POST', 'GET'])
@login_required
@permission_required(Permission.ADMINISTER)
def comments():
    page = request.args.get('page', 1, type=int)
    comments = Comments.query.order_by(Comments.date.desc())
    pagination =  comments.paginate(page=page, per_page=7, error_out=False)
    comments = pagination.items
    
    return render_template("/blogs/comments.html", comments=comments, 
                           pagination=pagination, permission=Permission, user=User)

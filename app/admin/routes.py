import logging

from flask import (Blueprint, render_template, redirect, 
                   url_for, flash, current_app, request)
from flask_login import login_required, current_user
from sqlalchemy import exc

from app import db
from ..auth import admin_required, permission_required
from ..auth.models import User, Role, Permission
from ..blogs.models import Posts, Comments, CommentReply, Tag
from ..main.models import Quotes, Feedback

from .forms import EditProfileAdminForm

admin_blueprint = Blueprint('admin', __name__, 
                            static_folder="admin", 
                            static_url_path="../static/admin/",
                            url_prefix="/admin")

@admin_blueprint.route("/")
@login_required
@permission_required(Permission.ADMINISTER)
def dashboard():
    user = User.query.get(current_user.id)
    form = EditProfileAdminForm(user=user)
    posts = Posts.query.order_by(Posts.date_created.desc())
    page = request.args.get('next')
    pagination = db.paginate(posts, page=page, per_page=10, error_out=False)
    return render_template("admin/dashboard.html", user=user, form=form)

@admin_blueprint.route("/boards")
@login_required
@admin_required
def boards():
    return render_template("admin/boards.html")

@admin_blueprint.route('/comments')
@login_required
@admin_required
def comments():
    comments = Comments.query.order_by(Comments.date.desc())
    page = request.args.get('page', type=int)
    pagination = db.paginate(comments, page=page, per_page=5, error_out=False)
    return render_template("admin/models/comments.html", comments=pagination.items,
                           pagination=pagination)

@admin_blueprint.route("/comment/enable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comments.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@admin_blueprint.route("/comment/disable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comments.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@admin_blueprint.route("/comment/delete/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_delete(id):
    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!.", category='info')
    
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@admin_blueprint.route("/@<string:username>/profile/", methods=['GET', 'POST'])
@login_required
@admin_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.bio = form.about_me.data
        try:
            db.session.add(user)
            db.session.commit()
            flash("User profile changed.", category="info")
            if user.is_administrator():
                return redirect(url_for(".profile", username=user.username))
            else:
                return redirect(url_for('users.user', username=user.username))
        except exc.IntegrityError as e:
            flash("User profile not changed", category="warning")
            logging.error("User profile could not changed: {}".format(e))
    form.email.data = user.email
    form.name.data = user.display_name
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.bio
    
    return render_template("admin/profile.html", form=form, user=user)

@admin_blueprint.route('/reports')
def reports():
    return "Hello"

@admin_blueprint.route("/tests/")
def tests():
    return "Hello"

@admin_blueprint.route("/users")
def users():
    bytens = User.query.order_by(User.last_seen.desc())
    page = request.args.get('page', type=int)
    pagination = db.paginate(bytens, page=page, per_page=5, error_out=False)
    return render_template("admin/models/users.html", users=pagination.items, pagination=pagination)

@admin_blueprint.route("/update/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.filter_by(user_id).first_or_404()
    return render_template("admin/users/edit.html", user=user)

@admin_blueprint.route("/restrict/<int:user_id>/", methods=['GET', 'PUT'])
@login_required
@admin_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template("admin/users/user.html")

@admin_blueprint.route("/remove/<int:user_id>/", methods=['GET', 'DELETE'])
@login_required
@admin_required
def remove_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"User with the username {user.username} removed.", category="info")
        return redirect(url_for('.users', page=1))
    except Exception as e:
        db.session.rollback()
        flash("User not removed!.", category="warning")
        raise e
     
@admin_blueprint.route("/quotes")
def quotes():
    qts = Quotes.query.order_by(Quotes.sent.desc())
    page = request.args.get('page', type=int)
    quts = db.paginate(qts, page=page, per_page=7, error_out=False)
    return render_template("admin/models/quotes.html", quotes=quts.items, pagin=quts)

@admin_blueprint.route("/feedback")
def feed():
    backfeed = Feedback.query.order_by(Feedback.created_at.desc())
    page = request.args.get('page', type=int)
    pagination = db.paginate(backfeed, page=page, per_page=5, error_out=False)
    return render_template("admin/models/feedback.html", feedback=pagination.items, pagin=pagination)

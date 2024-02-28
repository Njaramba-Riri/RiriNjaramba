from flask import Blueprint, render_template , url_for, abort

from ..auth.models import Permission, User, Role
from ..blogs.models import Posts, Comments

user_blueprint = Blueprint("users", __name__,
                           static_folder="static/users", template_folder="template/users",
                           url_prefix="/users/")

@user_blueprint.route('/@<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not user:
        abort(404)
    posts = user.posts.order_by(Posts.date_created.desc()).all()
    comments = user.comments.order_by(Comments.date.desc()).all()
    return render_template("/users/user.html", user=user, posts=posts, comments=comments)

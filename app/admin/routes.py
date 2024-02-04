import logging

from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import exc

from app import db
from ..auth import admin_required, permission_required
from ..auth.models import User, Role, Permission

from .forms import EditProfileAdminForm

admin_blueprint = Blueprint('admin', __name__,
                            static_folder="static/admin", 
                            template_folder="templates/admin",
                            url_prefix="/RiriNjaramba/admin")



@admin_blueprint.route("/")
@permission_required(Permission.ADMINISTER)
def dashboard():
    return "Hello there."


@admin_blueprint.route("/user-profile/<string:username>", methods=['POST', 'GET'])
def edit_user_profile(username):
    user = User.query.filter_by(username=username).first()
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash("User profile changed.", category="info")
            return redirect(url_for("users.user", username=user.username))
        except exc.IntegrityError as e:
            flash("User profile not changed", category="warning")
            logging.error("User profile could not changed: {}".format(e))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id

    return render_template("admin/edit-profile.html", form=form, user=user)
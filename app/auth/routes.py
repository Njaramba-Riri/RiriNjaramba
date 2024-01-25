from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

from app import db
from .form import LoginForm, RegisterForm
from .models import User


auth_blueprint = Blueprint("auth", __name__, 
                           static_folder="static/auth", template_folder="templates/auth", url_prefix="/RiriNjaramba/auth")

@auth_blueprint.route('/', methods=['POST', 'GET'])
def signin():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user, remember=form.remember.data)
        flash("You have logged in.", category="info")
        redirect(url_for('blogs.blog_index'))
    return render_template("auth/login.html", form=form)

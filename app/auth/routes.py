import logging

logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from sqlalchemy import exc

from app import db
from .form import LoginForm, RegisterForm, forgotPass, resetPassword
from .models import User

from ..email import send_email

auth_blueprint = Blueprint("auth", __name__, 
                           static_folder="static/auth", template_folder="templates/auth", url_prefix="/RiriNjaramba/auth")

@auth_blueprint.route('/', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        redirect('mainpp.index')
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            if next_url:
                return redirect(url_for(next_url))
            flash("Welcome, you have been logged in.", category="info")
            return redirect(url_for('blogs.blog_index'))
        else:
            flash("User with such username doesn't exist.", category="warning")
    return render_template("auth/login.html", form=form)

@auth_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if not current_user.is_anonymous:
        return redirect(url_for('mainapp.index'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        new_user = User()
        new_user.email = form.email.data
        new_user.username = form.username.data
        new_user.set_password(form.password.data)
        try:
            flash("{}".format(new_user), category="warning")
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            token = new_user.generate_confirmation_token()
            send_email(recipient=new_user.email, subject="Confirm Your Account", 
                       template="auth/email/confirm", user=new_user, token=token)
            flash("Thank you for registering, welcome to my blog", category="info")
            redirect(url_for('.signin'))
        except exc.IntegrityError as e:
            db.session.rollback()
            logger.error("Error while registerin user: {}".format(e))
            flash("Not able to create your account at the moment, kindly try later.", category="info")
    return render_template("auth/register.html", form=form)

@auth_blueprint.route('/confirm/<string:token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('mainapp.index'))
    if current_user.confirm_token(token):
        db.session.commit()
        flash("You have successfully confirmed your account, \
              it's my hope you will find the most out this place. Again, thank you", message="info")
    else:
        flash("The confirmation token have expired or is invalid.", category="warning") 
    return redirect(url_for('mainapp.index'))


@auth_blueprint.route('/resend_token')
@login_required
def resend_confirmation_token():
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email, subject="New Confirmation Token.",
               template="auth/email/confirm", token=token, user=current_user)
    flash("A new confirmation email has been sent to you just now, \
           kindly check your inbox; if not, check your spam folder.", category="info")
    return redirect(url_for('mainapp.index'))

@auth_blueprint.route('/forgot-password/', methods=['POST','GET'])
def forgotpass():
    if not current_user.is_anonymous:
        return redirect(url_for('mainapp.index'))
    form = forgotPass()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_pass_reset_token()
            send_email(to=user.email, subject="Password Reset Request.", 
                       template="auth/email/reset", user=user, token=token)
            flash("An email with reset instructions has just been sent to you.", category="info")
            return redirect(url_for('.signin'))
    return render_template("auth/forgot.html", form=form)


@auth_blueprint.route('password-reset/<string:token>/', methods=['POST', 'GET'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('mainapp.index'))
    form = resetPassword()
    if request.method == 'POST' and form.validate_on_submit():
        if User.confirm_reset_token(token, form.password.data):
            db.session.commit()
        flash("Your password has been changed successfully, you can now login.")
        return redirect(url_for('.signin'))
    return render_template("auth/passreset.html", form=form)

    
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mapp.index'))
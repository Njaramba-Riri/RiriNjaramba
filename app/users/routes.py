from flask import (Blueprint, render_template , url_for, 
                   abort, send_file, request, redirect, flash)
from flask_login import current_user

from app import db
from .forms import fileForm, aboutForm, updateBio
from ..auth.models import Permission, User, Role
from ..blogs.models import Posts, Comments

user_blueprint = Blueprint("users", __name__,
                           static_folder="static/users", template_folder="template/users",
                           url_prefix="/user/")

@user_blueprint.route('/@<string:username>/', methods=['POST', 'GET'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not user:
        abort(404)
    posts = user.posts.order_by(Posts.date_created.desc()).all()
    comments = user.comments.order_by(Comments.date.desc()).all()
    form = fileForm()
    about = aboutForm()
    bio = updateBio()
    if about.validate_on_submit():
        user.about = about.about.data
        try:
            db.session.add(user)
            db.session.commit()
            flash("Your professional summary was successfully updated", category="info")
            return redirect(url_for('.user', username=user.username))
        except Exception as e:
            db.session.rollback()
            flash(f"Oppsie!, about not updated: {e}", category="warning")
            
    if bio.validate_on_submit():
        user.display_name = bio.name.data
        user.location = bio.location.data
        user.interests = bio.interests.data
        user.bio = bio.bio.data
        try:
            db.session.add(user)
            db.session.commit()
            flash("Profile details changed succesfully.", category="info")
            return redirect(url_for('.user', username=user.username))
        except Exception as e:
            db.session.rollback()
            flash("Profile details not updated, try again later.", category="warning")
        
    if user.about:
        about.about.data = user.about
        bio.bio.data = user.bio
        bio.location.data = user.location
        bio.name.data = user.display_name
        bio.interests.data = user.interests
        
    return render_template("/users/user.html", user=user, about=about, bio=bio,
                           posts=posts, comments=comments, form=form, permission=Permission)

@user_blueprint.route('/upload-cv', methods=['GET','POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part", category="warning")
    
    file = request.files['file']
    
    if file.filename == '':
        flash("No file selected", category="warning")
    
    file.save("app/static/uploads/" + file.filename)
    flash("File uploaded successfully", category="info")
    
    return redirect(url_for('.user', username=current_user.username))

@user_blueprint.route('/')
def download_cv():
    file = "/home/riri/Desktop/RiriNjaramba/app/static/images/riri.jpg"
    
    return send_file(file, as_attachment=True)

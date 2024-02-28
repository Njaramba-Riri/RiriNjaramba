from flask import Blueprint, render_template, redirect, request, flash, abort, url_for
from flask_login import login_required
from .forms import FeedbackForm, quoteForm
from .models import Feedback, Quotes
from ..auth.models import User
from app import db

main_blueprint = Blueprint("mainapp", __name__,
                           static_folder='static/mainapp', template_folder='templates/mainapp',
                           url_prefix="/RiriNjaramba")

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        feed = form.feed.data
        
        details = Feedback(email=email, feed=feed)
        try:
            db.session.add(details)
            db.session.commit()
            flash("Thank you for contacting me, will be in touch shortly.", category="info")
        except Exception as e:
            db.session.rollback()
            flash(f"Something didn't go right, kindly try again: {e}", category="warning")
    return render_template('/mainapp/index.html', form=form)

@main_blueprint.route('/get-quote/', methods=['GET', 'POST'])
def quote():
    form = quoteForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        service = form.services.data
        description = form.more.data
        
        quote_obj = Quotes(name=name, email=email, service=service, description=description)
        try:
            db.session.add(quote_obj)
            db.session.commit()
            flash("Your quote has been received, I will be in touch in a few.", category="info")
            return redirect(url_for('.quote'))
        except Exception as e:
            db.session.rollback()
            flash("Quote not sent, kindly try again.", category="warning")
    return render_template('/mainapp/quote.html', form=form)

@main_blueprint.route('/projects', methods=['GET', 'POST'])
def projects():
    feedback = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("/mainapp/projects.html", feedback=feedback)

@main_blueprint.route('/lets-talk', methods=['GET', 'POST'])
def letstalk():
    return render_template("/mainapp/chat.html")

@main_blueprint.route("/resources")
def resources():
    return render_template("/mainapp/resources.html")

@main_blueprint.route("/user/<string:username>/")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not user:
        abort(404)
    return render_template("/users/user.html", user=user)

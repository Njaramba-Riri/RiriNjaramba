from flask import Blueprint, render_template, redirect, request, flash
from .forms import FeedbackForm
from .models import Feedback
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
            flash("Thank you for contacting me, will be in touch shortly.")
        except Exception as e:
            db.session.rollback()
            flash("Something didn't go right, kindly try again.")
    return render_template('/mainapp/index.html', form=form)
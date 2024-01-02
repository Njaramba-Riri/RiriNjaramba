from flask import Blueprint, render_template, redirect

main_blueprint = Blueprint("mainapp", __name__,
                           static_folder='static/mainapp', template_folder='templates/mainapp',
                           url_prefix="/RiriNjaramba")

@main_blueprint.route('/home')
def index():
    return render_template('/mainapp/index.html')
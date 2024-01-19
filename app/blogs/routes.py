from flask import Blueprint, render_template, url_for
from app import db

blog_blueprint = Blueprint("blogs", __name__, static_folder="/blogs/static",
                           template_folder="/templates/blogs", url_prefix="/RiriNjaramba/blogs/")

@blog_blueprint.route('/', methods=['POST'])
def blog_index():
    return render_template("blogs/index.html")
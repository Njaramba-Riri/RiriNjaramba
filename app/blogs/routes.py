import logging

logging.basicConfig(format=("%(asctime)s: %(name)s:%(levelname)s: %(message)s"))
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, url_for, request
from app import db

from .models import Posts, Comments
from .forms import CommentForm

blog_blueprint = Blueprint("blogs", __name__, static_folder="/blogs/static",
                           template_folder="/templates/blogs", url_prefix="/RiriNjaramba/blogs/")

@blog_blueprint.route('/', methods=['GET', 'POST'])
def blog_index():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_created.desc())
    blogs = db.paginate(posts, page=page, per_page=4, error_out=False)
    next_url = url_for('blogs.blog_index', page=blogs.next_num) if blogs.has_next else None
    prev_url = url_for('blogs.blog_index', page=blogs.prev_num) if blogs.has_prev else None
    return render_template("blogs/index.html", posts=blogs.items,
                           next=next_url, prev=prev_url)
 
@blog_blueprint.route("/<string:title>", methods=["POST", "GET"])
def blog(title):
    post = Posts.query.filter_by(title=title).first_or_404()
    form = CommentForm()
    if request.method == 'POST' and form.validate():
        comment = Comments()

        comment.email = form.email.data
        comment.name = form.name.data
        comment.comment = form.comment.data
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            logger.info("Error while adding comment: {}".format(e))
            db.session.rollback()
    return render_template("blogs/blog.html", blog=post, form=form)
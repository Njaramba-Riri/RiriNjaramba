from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown

from config import DevConfig

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug = DebugToolbarExtension()
moment = Moment()
bootstrap = Bootstrap()
pagedown = PageDown()

def forbidden_access(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            "Error": "Forbidden Access."
        })
        response.status_code = 403
    return render_template('/errors/403.html'), 403

def not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({
            "Error": "Resource not found."
        })
        response.status_code = 404
    return render_template("/errors/404.html"), 404

def method_not_allowed(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            "Error": "Method Not Allowed."
        })
        response.status_code = 405
    return render_template('/errors/405.html'), 405

def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            "Error": "An internal server error occured."
        })
        response.status_code = 500
    return render_template("errors/serverr.html"), 500
def create_app(object):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    moment.init_app(app)
    #bootstrap.init_app(app)
    pagedown.init_app(app)
    debug.init_app(app)


    from .main import create_app as mainapp_create_module
    from .blogs import create_app as blog_create_app
    from .auth import create_app as auth_create_app
    from .admin import create_app as admin_create_app
    from .users import create_app as users_create_app

    mainapp_create_module(app)
    blog_create_app(app)
    auth_create_app(app)
    admin_create_app(app)
    users_create_app(app)
    
    app.register_error_handler(403, forbidden_access)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)
 

    return app

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from config import DevConfig

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({
            "Error": "Resource not found."
        })
        response.status_code = 404
    return render_template("/errors/404.html")


def create_app(object):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    from .main import create_app as mainapp_create_module

    mainapp_create_module(app)

    app.register_error_handler(404, not_found)

    return app
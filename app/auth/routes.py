from flask import Blueprint, render_template, redirect, url_for, flash

from app import db

auth_blueprint = Blueprint("auth", __name__, 
                           static_folder="static/auth", template_folder="templates/auth", url_prefix="/RiriNjaramba/auth")

@auth_blueprint.route('/', methods=['POST', 'GET'])
def signin():
    return "Sign in page."

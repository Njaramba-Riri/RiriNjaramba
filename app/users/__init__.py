def create_app(app, **kwargs):
    from .routes import user_blueprint
    app.register_blueprint(user_blueprint)
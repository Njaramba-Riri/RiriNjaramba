def create_app(app, **kwargs):
    from .routes import blog_blueprint
    app.register_blueprint(blog_blueprint)

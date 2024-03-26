def create_app(app, **kwargs):
    from .routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

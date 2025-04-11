from .auth_routes import auth_bp
from .protected_routes import protected_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)

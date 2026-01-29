"""
Route registration module
"""

def register_blueprints(app):
    """Register all blueprints to the app"""
    from routes.auth import auth_bp

    # Register blueprints with URL prefix
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    print("All blueprints registered successfully")

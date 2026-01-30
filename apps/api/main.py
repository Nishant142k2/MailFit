"""
MailFit API - Main Application
Run with: uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__)

def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://mailfit:mailfit123@localhost:5432/mailfit_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Email config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Configure Celery
    celery.conf.update(
        broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        timezone='UTC',
        enable_utc=True,
    )

    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)

    # Health check
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        })

    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # For direct Python execution (not recommended for production)
    app.run(host='0.0.0.0', port=5000, debug=True)

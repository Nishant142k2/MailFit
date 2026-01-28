# init_db.py
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

from api.main import create_app, db
from api.models import User  # Import all your models

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

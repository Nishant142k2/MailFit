from main import create_app, db
import models  # CRITICAL: registers User & OTPLog

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully")

"""
Database models
"""

from main import db
from datetime import datetime, timedelta
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # OTP related fields
    otp_code = db.Column(db.String(6))
    otp_expires_at = db.Column(db.DateTime)
    otp_attempts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def generate_otp(self):
        """Generate 6-digit OTP and set expiration"""
        self.otp_code = f"{secrets.randbelow(1000000):06d}"
        self.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        self.otp_attempts = 0
        return self.otp_code

    def verify_otp(self, otp):
        """Verify OTP and check expiration"""
        # Check if OTP has expired
        if self.otp_expires_at and datetime.utcnow() > self.otp_expires_at:
            return False, "OTP expired. Please request a new one."

        # Check attempt limit
        if self.otp_attempts >= 3:
            return False, "Too many failed attempts. Please request a new OTP."

        # Verify OTP code
        if self.otp_code == otp:
            self.is_verified = True
            self.otp_code = None
            self.otp_expires_at = None
            self.otp_attempts = 0
            return True, "Verified successfully"
        else:
            self.otp_attempts += 1
            remaining = 3 - self.otp_attempts
            return False, f"Invalid OTP. {remaining} attempt(s) remaining."

class OTPLog(db.Model):
    __tablename__ = 'otp_logs'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False)  # 'register', 'login', 'verify_success', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))

    def __repr__(self):
        return f'<OTPLog {self.email} - {self.action}>'

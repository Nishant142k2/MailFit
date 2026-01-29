"""
Authentication routes with OTP verification
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import re
from main import db, mail
from models import User, OTPLog
from tasks import send_otp_email

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Check if password meets requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with OTP verification

    Request Body:
        {
            "email": "user@example.com",
            "username": "username",
            "password": "Password123"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password')

        # Validate input
        if not email or not username:
            return jsonify({'error': 'Email and username are required'}), 400

        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400

        # Check password if provided
        if password:
            is_strong, message = is_strong_password(password)
            if not is_strong:
                return jsonify({'error': message}), 400

        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            if existing_user.is_verified:
                return jsonify({'error': 'User already exists with this email or username'}), 409
            else:
                # User exists but not verified, update and resend OTP
                user = existing_user
                if password:
                    user.set_password(password)
        else:
            # Create new user
            user = User(email=email, username=username)
            if password:
                user.set_password(password)
            db.session.add(user)

        # Generate OTP
        otp = user.generate_otp()
        db.session.commit()

        # Log OTP request
        otp_log = OTPLog(
            email=email,
            action='register',
            ip_address=request.remote_addr
        )
        db.session.add(otp_log)
        db.session.commit()

        # Send OTP email asynchronously
        send_otp_email.delay(email, otp, 'registration')

        return jsonify({
            'message': 'OTP sent to your email. Please verify within 10 minutes.',
            'email': email,
            'expires_in': '10 minutes'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP for registration

    Request Body:
        {
            "email": "user@example.com",
            "otp": "123456"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()

        # Validate input
        if not email or not otp:
            return jsonify({'error': 'Email and OTP are required'}), 400

        if len(otp) != 6 or not otp.isdigit():
            return jsonify({'error': 'OTP must be a 6-digit number'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.is_verified:
            return jsonify({'error': 'User already verified'}), 400

        # Verify OTP
        success, message = user.verify_otp(otp)

        if success:
            db.session.commit()

            # Log successful verification
            otp_log = OTPLog(
                email=email,
                action='verify_success',
                ip_address=request.remote_addr
            )
            db.session.add(otp_log)
            db.session.commit()

            return jsonify({
                'message': message,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_verified': user.is_verified
                }
            }), 200
        else:
            db.session.commit()

            # Log failed verification
            otp_log = OTPLog(
                email=email,
                action='verify_failed',
                ip_address=request.remote_addr
            )
            db.session.add(otp_log)
            db.session.commit()

            return jsonify({'error': message}), 400

    except Exception as e:
        db.session.rollback()
        print(f"OTP verification error: {str(e)}")
        return jsonify({'error': 'Verification failed', 'details': str(e)}), 500

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """
    Resend OTP for registration

    Request Body:
        {
            "email": "user@example.com"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user or user.is_verified:
            return jsonify({'error': 'Invalid request. User may already be verified.'}), 400

        # Rate limiting: Check if OTP was sent recently
        recent_log = OTPLog.query.filter_by(
            email=email,
            action='register'
        ).order_by(OTPLog.created_at.desc()).first()

        if recent_log:
            time_diff = datetime.utcnow() - recent_log.created_at
            if time_diff.total_seconds() < 60:
                wait_time = 60 - int(time_diff.total_seconds())
                return jsonify({
                    'error': f'Please wait {wait_time} seconds before requesting another OTP'
                }), 429

        # Generate new OTP
        otp = user.generate_otp()
        db.session.commit()

        # Log OTP request
        otp_log = OTPLog(
            email=email,
            action='resend_otp',
            ip_address=request.remote_addr
        )
        db.session.add(otp_log)
        db.session.commit()

        # Send OTP email
        send_otp_email.delay(email, otp, 'registration')

        return jsonify({
            'message': 'OTP resent successfully',
            'expires_in': '10 minutes'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Resend OTP error: {str(e)}")
        return jsonify({'error': 'Failed to resend OTP', 'details': str(e)}), 500

@auth_bp.route('/login-request', methods=['POST'])
def login_request():
    """
    Request OTP for login (passwordless login)

    Request Body:
        {
            "email": "user@example.com"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if not user.is_verified:
            return jsonify({'error': 'Please verify your email first'}), 403

        # Rate limiting
        recent_log = OTPLog.query.filter_by(
            email=email,
            action='login'
        ).order_by(OTPLog.created_at.desc()).first()
        
        if recent_log:
            time_diff = datetime.utcnow() - recent_log.created_at
            if time_diff.total_seconds() < 60:
                wait_time = 60 - int(time_diff.total_seconds())
                return jsonify({
                    'error': f'Please wait {wait_time} seconds before requesting another OTP'
                }), 429
         # Generate OTP
        otp = user.generate_otp()
        db.session.commit()

        # Log OTP request
        otp_log = OTPLog(
            email=email,
            action='login',
            ip_address=request.remote_addr
        )
        db.session.add(otp_log)
        db.session.commit() 
        
        # Send OTP email
        send_otp_email.delay(email, otp, 'login')

        return jsonify({
            'message': 'Login OTP sent successfully',
            'expires_in': '10 minutes'
        }), 200 
        
    except Exception as e:
        db.session.rollback()
        print(f"Login OTP error: {str(e)}")
        return jsonify({'error': 'Failed to send login OTP', 'details': str(e)}), 500


            

"""
Celery tasks for background processing
Run worker with: celery -A tasks.celery worker --loglevel=info
"""

from main import celery, mail
from flask_mail import Message

@celery.task
def send_otp_email(email, otp, purpose):
    """
    Send OTP email asynchronously

    Args:
        email (str): Recipient email address
        otp (str): 6-digit OTP code
        purpose (str): Purpose of OTP ('registration', 'login', 'password_reset')
    """
    try:
        subject = f"MailFit - {purpose.title()} OTP Code"

        body = f"""
        Hello,

        Your MailFit {purpose} OTP code is: {otp}

        This code will expire in 10 minutes.

        If you didn't request this OTP, please ignore this email or contact support.

        Best regards,
        MailFit Team
        """

        msg = Message(
            subject=subject,
            recipients=[email],
            body=body
        )

        mail.send(msg)
        print(f" OTP email sent to {email}")
        return {'status': 'success', 'email': email}

    except Exception as e:
        print(f" Failed to send OTP email to {email}: {str(e)}")
        raise

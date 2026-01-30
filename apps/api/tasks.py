"""
Celery tasks for background processing
"""

from flask_mail import Message
from main import celery, mail, create_app

# Create Flask app ONCE for the Celery worker
flask_app = create_app()

@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_otp_email(self, email, otp, purpose):
    """
    Send OTP email asynchronously
    """
    with flask_app.app_context():  # 🔥 THIS IS THE KEY
        subject = f"MailFit - {purpose.title()} OTP Code"

        body = f"""
Hello,

Your MailFit {purpose} OTP code is: {otp}

This code will expire in 10 minutes.

If you didn't request this OTP, please ignore this email.

Best regards,
MailFit Team
"""

        msg = Message(
            subject=subject,
            recipients=[email],
            body=body,
        )

        mail.send(msg)
        print(f"✅ OTP email sent to {email}")

        return {"status": "success", "email": email}

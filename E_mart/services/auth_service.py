from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.core.cache import cache

def save_otp(email, otp):
    return cache.set(f"otp_{email}", otp, timeout=300)

def check_otp(email, otp):
    stored_otp = cache.get(f"otp_{email}")
    print(stored_otp)
    if stored_otp and stored_otp == otp:
        cache.delete(f"otp_{email}") 
        return True
    return False

    
def generate_secure_otp(length=6):
    """Generates a cryptographically secure numeric OTP."""
    digits = '0123456789'
    return ''.join(secrets.choice(digits) for _ in range(length))


def send_otp_to_email(to_email, otp):
    print("hello")
    subject = 'Your Verification OTP'
    message = f'Your OTP for email verification is: {otp}. Please use this OTP to verify your email address.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    print(subject,message, from_email, recipient_list)
    send_mail(subject, message, from_email, recipient_list)
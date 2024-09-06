from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.conf import settings
from .utils import Util

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # reset_url = f"{settings.FRONTEND_DOMAIN}/password-reset-confirm/{reset_password_token.key}"
    reset_url = f"http://localhost:8000/api/password_reset/confirm/{reset_password_token.key}"
    
    # Email data
    email_data = {
        'email_subject': 'Password Reset Request',
        'email_body': f"Hello,\nPlease use the following link to reset your password: {reset_url}",
        'to_email': reset_password_token.user.email,
    }

    Util.send_email(email_data)

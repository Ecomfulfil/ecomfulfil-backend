from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_reset_password_email(user, token):
    subject = 'Reset Your Password'
    from_email = settings.EMAIL_FROM
    to_email = [user.email]
    reset_link = f"{settings.CLIENT_URL}/reset-password?token={token}"
    context = {
        'user': user,
        'reset_link': reset_link,
    }
    text_content = render_to_string('emails/reset_password_email.html', context)
    html_content = render_to_string('emails/reset_password_email.html', context)
    send_email(subject, text_content, html_content, from_email, to_email)


def send_verification_email(user, token):
    subject = 'Verify Your Email Address'
    from_email = settings.EMAIL_FROM
    to_email = [user.email]
    verification_link = f"{settings.CLIENT_URL}/verify-email?token={token}"
    context = {
        'user': user,
        'verification_link': verification_link,
    }
    text_content = render_to_string('emails/verification_email.html', context)
    html_content = render_to_string('emails/verification_email.html', context)
    send_email(subject, text_content, html_content, from_email, to_email)


def send_email(subject, text_content, html_content, from_email, to_email):
    """
    Sends an HTML email with the provided details.
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

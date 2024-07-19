from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_password_reset_email(user_email, reset_url):
    """
    Sends a password reset email to the provided user email address.
    """
    subject = "Reset Your Password"
    context = {"reset_url": reset_url}
    html_content = render_to_string("password_reset_email.html", context)
    send_html_email(subject, html_content, settings.EMAIL_FROM, [user_email])


def send_html_email(subject, html_content, email_from, recipient_list):
    """
    Sends an HTML email with the provided details.
    """
    print(email_from, recipient_list)
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=email_from,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.to = recipient_list
    msg.send()

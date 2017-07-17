from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(
    subject,
    to,
    template_name,
    context,
    fail_silently=False,
    from_email=settings.DEFAULT_FROM_EMAIL,
    headers=None,
):
    """
    Send an email created from a template
    """
    message_html = render_to_string(template_name, context)
    message_txt = striptags(message_html)
    email = EmailMultiAlternatives(
        body=message_txt,
        from_email=from_email,
        headers=headers,
        subject=subject,
        to=to,
    )
    email.attach_alternative(message_html, 'text/html')
    email.send(fail_silently=fail_silently)

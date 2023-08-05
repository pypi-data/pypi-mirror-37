from typing import List, Optional, Tuple

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(
    subject, message, recipient: str,
    attachments: Optional[List[Tuple[str, bytes]]] = None
):
    mail = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient],
        attachments=attachments
    )
    mail.attach_alternative(message, 'text/html')
    return mail.send()


def send_template_email(
    template_name, context, subject, recipient: str,
    attachments: Optional[List[Tuple[str, bytes]]] = None
):
    message = render_to_string(template_name, context=context)
    send_email(
        subject=subject,
        message=message,
        recipient=recipient,
        attachments=attachments
    )

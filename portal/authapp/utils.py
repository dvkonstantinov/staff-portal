import re

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Только домен ilaaspect.com
EMAIL_PATTERN = r'^[a-zA-Z0-9_\.-]*@ilaaspect\.com$'

account_activation_token = default_token_generator


def check_email_pattern(email):
    pattern = re.compile(EMAIL_PATTERN)
    return pattern.match(email)


def send_verification_email(user):
    mail_subject = 'Активация аккаунта на портале ILA ASEPCT.'
    message = render_to_string(
        'authapp/messages/email_verification_message.txt', {
            'user': user,
            'domain': settings.SITE_DOMAIN,
            'protocol': settings.SITE_PROTOCOL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
    to_email = user.email
    is_success_mail = send_mail(mail_subject,
                                message,
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[to_email],
                                fail_silently=True
                                )
    return is_success_mail

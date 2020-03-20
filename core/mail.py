from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def envia_email_template(assunto, nome_template, contexto, lista_envio,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         fail_silently=False):
    message_html = render_to_string(nome_template, contexto)
    message_txt = striptags(message_html)
    email = EmailMultiAlternatives(
        subject=assunto,
        body=message_txt,
        from_email=from_email,
        to=lista_envio
    )

    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)

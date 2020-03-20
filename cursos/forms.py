from django import forms
from django.conf import settings
from core.mail import envia_email_template


class ContatoCurso(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def envia_email(self, curso):
        assunto = 'Contato Curso [%s]' % curso

        contexto = {
            'nome': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'assunto': assunto,
            'mensagem': self.cleaned_data['mensagem'],
        }

        envia_email_template(
            assunto, 'cursos/contato_email.html', contexto,
            [settings.EMAIL_CONTATO],
            settings.DEFAULT_FROM_EMAIL,
        )

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from core.mail import envia_email_template
from core.utils import generate_hash_key
from .models import PasswordReset

User = get_user_model()


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha',
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("passowrd1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Confirmação de Senha está incorreta!')
        return password2

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário foi encontrado com este E-mail !'
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()

        context = {
            'reset': reset,
        }

        envia_email_template(
            'Nova Senha', 'mail_password_reset.html', context, [user.email]
        )


class EditCadastroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name']

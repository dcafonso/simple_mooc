from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    SetPasswordForm,
)
from .forms import (
    RegistroForm,
    EditCadastroForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from .models import PasswordReset

User = get_user_model()


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistroForm()

    context = {
        'form': form
    }

    return render(request, 'registro.html', context)


@login_required
def edit_cadastro(request):
    context = {}
    if request.method == 'POST':
        form = EditCadastroForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditCadastroForm(instance=request.user)
            context['success'] = True
    else:
        form = EditCadastroForm(instance=request.user)
    context['form'] = form
    return render(request, 'edit_usuario.html', context)


def password_reset(request):
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, 'reset_password.html', context)


def password_reset_confirm(request, key):
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, 'password_reset_confirm.html', context)


@login_required
def edit_senha(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, 'edit_password.html', context)

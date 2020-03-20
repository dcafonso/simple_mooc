from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import (
    RegistroForm,
    EditCadastroForm,
    PasswordChangeForm,
)


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

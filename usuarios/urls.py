from django.urls import re_path
from django.contrib.auth import views as auth_views
from usuarios.views import (
    register,
    dashboard,
    edit_cadastro,
    edit_senha,
)


urlpatterns = [
    re_path(r'^dashboard/$', dashboard, name='usuarios_dashboard'),
    re_path(r'^entrar/$',
            auth_views.LoginView.as_view(template_name='login.html'),
            name='usuarios_login'),
    re_path(r'^sair/$', auth_views.LogoutView.as_view(next_page='core_home'),
            name='usuarios_logout'),
    re_path(r'^cadastro/$', register, name='usuarios_registro'),
    re_path(r'^editar-cadastro/$', edit_cadastro,
            name='usuarios_edit'),
    re_path(r'^editar-senha/$', edit_senha,
            name='usuarios_edit_senha'),
]

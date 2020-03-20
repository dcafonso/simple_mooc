from django.urls import re_path

from .views import (
    home,
    contato,
)


urlpatterns = [
    re_path(r'^$', home, name='core_home'),
    re_path(r'^contato/$', contato, name='core_contato'),
]

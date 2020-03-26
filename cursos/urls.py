from django.urls import re_path

from .views import (
    cursos,
    detalhe_curso,
    inscricao_curso,
)


urlpatterns = [
    re_path(r'^cursos/$', cursos, name='cursos_curso'),
    re_path(r'^detalhe-curso/(?P<slug>[\w_-]+)/$',
            detalhe_curso, name='cursos_detalhe'),
    re_path(r'înscricao/(?P<slug>[\w_-]+)/$', inscricao_curso,
            name='cursos_inscricao'),
]

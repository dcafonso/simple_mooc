from django.urls import re_path

from .views import (
    cursos,
    detalhe_curso,
    inscricao_curso,
    anuncios_curso,
    mostrar_anuncios_curso,
    cancela_inscricao
)


urlpatterns = [
    re_path(r'^cursos/$', cursos, name='cursos_curso'),
    re_path(r'^detalhe-curso/(?P<slug>[\w_-]+)/$',
            detalhe_curso, name='cursos_detalhe'),
    re_path(r'înscricao/(?P<slug>[\w_-]+)/$', inscricao_curso,
            name='cursos_inscricao'),
    re_path(r'cancela_inscricao/(?P<slug>[\w_-]+)/$', cancela_inscricao,
            name='cursos_cancela_inscricao'),
    re_path(r'anuncios/(?P<slug>[\w_-]+)/$', anuncios_curso,
            name='cursos_anuncios'),
    re_path(r'anuncios/(?P<slug>[\w_-]+)/(?P<pk>\d+)/$',
            mostrar_anuncios_curso,
            name='cursos_mostra_anuncios'),
]

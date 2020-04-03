from django.urls import re_path

from .views import (
    cursos,
    detalhe_curso,
    inscricao_curso,
    anuncios_curso,
    mostrar_anuncios_curso,
    cancela_inscricao,
    aulas,
    acessar_aula,
    material
)


urlpatterns = [
    re_path(r'^cursos/$', cursos, name='cursos_curso'),
    re_path(r'^detalhe-curso/(?P<slug>[\w_-]+)/$',
            detalhe_curso, name='cursos_detalhe'),
    re_path(r'înscricao/(?P<slug>[\w_-]+)/$', inscricao_curso,
            name='cursos_inscricao'),
    re_path(r'cancela_inscricao/(?P<slug>[\w_-]+)/$', cancela_inscricao,
            name='cursos_cancela_inscricao'),
    re_path(r'(?P<slug>[\w_-]+)/anuncios/$', anuncios_curso,
            name='cursos_anuncios'),
    re_path(r'(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$',
            mostrar_anuncios_curso,
            name='cursos_mostra_anuncios'),
    re_path(r'(?P<slug>[\w_-]+)/aulas/$', aulas,
            name='cursos_aulas'),
    re_path(r'(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', acessar_aula,
            name='cursos_acessa_aula'),
    re_path(r'(?P<slug>[\w_-]+)/aulas/material/(?P<pk>\d+)/$', material,
            name='cursos_material'),
]

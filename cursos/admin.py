from django.contrib import admin
from .models import (
    Curso,
    InscricaoCurso,
    AnunciosCurso,
    Comentario,
)


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'descricao']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Curso, CursoAdmin)
admin.site.register([InscricaoCurso, AnunciosCurso, Comentario])

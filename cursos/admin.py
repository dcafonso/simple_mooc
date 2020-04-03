from django.contrib import admin
from .models import (
    Curso,
    InscricaoCurso,
    AnunciosCurso,
    Comentario,
    Aula,
    Material
)


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'descricao']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


class MaterialInlineAdmin(admin.StackedInline):
    model = Material


class AulaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nro_aula', 'curso', 'data_liberacao']
    search_fields = ['titulo', 'descricao']
    list_filter = ['created_at']
    inlines = [MaterialInlineAdmin]


admin.site.register(Curso, CursoAdmin)
admin.site.register([InscricaoCurso, AnunciosCurso, Comentario])
admin.site.register(Aula, AulaAdmin)

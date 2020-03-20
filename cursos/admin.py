from django.contrib import admin
from .models import (
    Curso,
)


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'descricao']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Curso, CursoAdmin)

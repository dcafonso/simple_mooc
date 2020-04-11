from django.contrib import admin
from .models import (
    Topicos,
    Respostas
)


class TopicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'created_at', 'updated_at']
    search_fields = ['titulo', 'autor']
    prepopulate_fields = {'slug': ('titulo',)}


class RespostaAdmin(admin.ModelAdmin):
    list_display = ['resposta', 'autor', 'created_at', 'updated_at']
    search_fields = ['resposta', 'autor']


admin.site.register(Topicos, TopicoAdmin)
admin.site.register(Respostas, RespostaAdmin)

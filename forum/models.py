from django.db import models
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager


class Topicos(models.Model):
    titulo = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    conteudo = models.TextField('Mensagem')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='topicos',
        on_delete=models.CASCADE
    )
    visualizacoes = models.IntegerField('Visualizações', default=0)
    resposta = models.IntegerField('Respostas', default=0)
    tags = TaggableManager()
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('forum_topico', args=[self.slug])

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']


class Respostas(models.Model):
    resposta = models.TextField('Resposta')
    topico = models.ForeignKey(
        Topicos,
        verbose_name='Tópico',
        related_name='respostas',
        on_delete=models.CASCADE
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='respostas',
        on_delete=models.CASCADE
    )
    correta = models.BooleanField('Correta?', blank=True, default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.resposta[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correta', 'created_at']

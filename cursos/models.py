from django.db import models
from django.urls import reverse


class CursoManager(models.Manager):
    def busca(self, query):
        return self.get_queryset().filter(
            models.Q(nome__icontains=query) |
            models.Q(descricao__icontains=query)
        )


class Curso(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    descricao = models.TextField('Descrição', blank=True)
    sobre = models.TextField('Sobre o Curso', blank=True)
    data_inicio = models.DateField('Data de Início', blank=True, null=True)
    imagem = models.ImageField(
        upload_to='cursos/imagens',
        verbose_name='Imagem',
        blank=True, null=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CursoManager()

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('cursos_detalhe', args=[self.slug])

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from core.mail import envia_email_template


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

    def aulas_liberadas(self):
        today = timezone.now().date()
        return self.aulas.filter(data_liberacao__gte=today)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('cursos_detalhe', args=[self.slug])


class Aula(models.Model):
    titulo = models.CharField('Título', max_length=100)
    descricao = models.CharField('Descrição', max_length=150, blank=True)
    nro_aula = models.IntegerField('Nro. Aula', blank=True, default=0)
    data_liberacao = models.DateField('Data Liberação', blank=True, null=True)
    curso = models.ForeignKey(
        Curso,
        verbose_name='Curso',
        related_name='aulas',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def is_disponivel(self):
        if self.data_liberacao:
            today = timezone.now().date()
            return self.data_liberacao >= today

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['nro_aula']


class Material(models.Model):
    nome = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Mídia', blank=True)
    arquivo = models.FileField(
        upload_to='aulas/materiais',
        blank=True,
        null=True
    )
    aula = models.ForeignKey(
        Aula,
        verbose_name='Aula',
        related_name='materiais',
        on_delete=models.CASCADE
    )

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


class InscricaoCurso(models.Model):
    STATUS_CHOICE = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='inscrições',
        on_delete=models.CASCADE
    )
    curso = models.ForeignKey(
        Curso,
        verbose_name='Curso',
        related_name='inscrições',
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        'Situação',
        choices=STATUS_CHOICE,
        default=0,
        blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_aprovado(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'curso'), )


class AnunciosCurso(models.Model):
    curso = models.ForeignKey(
        Curso,
        verbose_name='Curso',
        related_name='anuncios',
        on_delete=models.CASCADE
    )
    titulo = models.CharField('Título', max_length=100)
    conteudo = models.TextField('Conteúdo')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comentario(models.Model):
    anuncio = models.ForeignKey(
        AnunciosCurso,
        verbose_name='Anúncio',
        related_name='comentarios',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='usuário',
        on_delete=models.CASCADE
    )
    comentario = models.TextField('Comentário')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']


def post_save_anuncios(instance, created, **kwargs):
    if created:
        assunto = instance.titulo

        context = {
            'anuncio': instance
        }

        inscricoes = InscricaoCurso.objects.filter(
            curso=instance.curso,
            status=1
        )
        for inscricao in inscricoes:
            lista_emails = [inscricao.user.email]
        envia_email_template(
            assunto,
            'cursos/email_anuncios.html',
            context,
            lista_emails
        )


models.signals.post_save.connect(
    post_save_anuncios,
    sender=AnunciosCurso,
    dispatch_uid='post_save_anuncios'
)

from django.template import Library
from cursos.models import InscricaoCurso

register = Library()


@register.inclusion_tag('cursos/templatetags/meus_cursos.html')
def meus_cursos(user):
    inscricoes = InscricaoCurso.objects.filter(user=user)
    context = {
        'inscricoes': inscricoes
    }
    return context


@register.simple_tag
def carrega_meus_cursos(user):
    return InscricaoCurso.objects.filter(user=user)

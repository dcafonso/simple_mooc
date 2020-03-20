from django.shortcuts import render
from cursos.models import Curso


def home(request):
    cursos = Curso.objects.all()
    return render(request, 'core/index.html', {'cursos': cursos})


def contato(request):
    return render(request, 'core/contato.html')

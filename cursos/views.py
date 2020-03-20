from django.shortcuts import render, get_object_or_404
from .models import Curso
from .forms import ContatoCurso


def cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/cursos.html', {'cursos': cursos})


def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    contexto = {}

    if request.method == 'POST':
        form = ContatoCurso(request.POST)
        if form.is_valid():
            contexto['is_valid'] = True

            form.envia_email(curso)
            form = ContatoCurso()
    else:
        form = ContatoCurso()

    contexto['curso'] = curso
    contexto['form'] = form

    return render(request, 'cursos/detalhe_curso.html', contexto)

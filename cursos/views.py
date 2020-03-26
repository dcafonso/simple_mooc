from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, InscricaoCurso
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


@login_required
def inscricao_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    inscricao, created = InscricaoCurso.objects.get_or_create(
        user=request.user,
        curso=curso
    )
    if created:
        inscricao.active()
        messages.success(request, 'Inscrição efetuada com sucesso.')
    else:
        messages.info(request, 'Você já está inscrito neste curso.')
    return redirect('usuarios_dashboard')

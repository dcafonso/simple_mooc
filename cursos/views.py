from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, InscricaoCurso
from .forms import ContatoCurso, ComentarioForm


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


@login_required
def cancela_inscricao(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    inscricao = get_object_or_404(
        InscricaoCurso,
        user=request.user,
        curso=curso
    )
    if request.method == 'POST':
        inscricao.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('usuarios_dashboard')
    context = {
        'inscricao': inscricao,
        'curso': curso,
    }
    return render(request, 'cursos/cancela_inscricao.html', context)


@login_required
def anuncios_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)

    if not request.user.is_staff:
        inscricao = get_object_or_404(
            InscricaoCurso,
            user=request.user,
            curso=curso
        )
        if not inscricao.is_aprovado():
            messages.error(request, 'Sua inscrição está pendente!')
            return redirect('usuarios_dashboard')

    context = {
        'curso': curso,
        'anuncios': curso.anuncios.all(),
    }

    return render(request, 'cursos/anuncios_curso.html', context)


@login_required
def mostrar_anuncios_curso(request, slug, pk):
    curso = get_object_or_404(Curso, slug=slug)

    if not request.user.is_staff:
        inscricao = get_object_or_404(
            InscricaoCurso,
            user=request.user,
            curso=curso
        )
        if not inscricao.is_aprovado():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('usuarios_dashboard')

    anuncios = get_object_or_404(curso.anuncios.all(), pk=pk)

    form = ComentarioForm(request.POST or None)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.user = request.user
        comentario.anuncio = anuncios
        comentario.save()
        form = ComentarioForm()
        messages.success(request, 'Seu comentário foi registrado com sucesso.')

    context = {
        'curso': curso,
        'anuncios': anuncios,
        'form': form,
    }
    return render(request, 'cursos/mostrar_anuncios_curso.html', context)

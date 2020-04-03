from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, InscricaoCurso, Aula, Material
from .forms import ContatoCurso, ComentarioForm
from .decorators import inscricao_required


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
@inscricao_required
def anuncios_curso(request, slug):
    curso = request.curso

    context = {
        'curso': curso,
        'anuncios': curso.anuncios.all(),
    }

    return render(request, 'cursos/anuncios_curso.html', context)


@login_required
@inscricao_required
def mostrar_anuncios_curso(request, slug, pk):
    curso = request.curso
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


@login_required
@inscricao_required
def aulas(request, slug):
    curso = request.curso
    aulas = curso.aulas_liberadas()
    if request.user.is_staff:
        aulas = curso.aulas.all()
    context = {
        'curso': curso,
        'aulas': aulas
    }
    return render(request, 'cursos/aulas.html', context)


@login_required
@inscricao_required
def acessar_aula(request, slug, pk):
    curso = request.curso
    aula = get_object_or_404(Aula, pk=pk, curso=curso)
    if not request.user.is_staff and not aula.is_disponivel():
        messages.error(request, 'Esta aula não está disponível.')
        redirect('cursos_aulas', slug=curso.slug)

    context = {
        'curso': curso,
        'aula': aula
    }

    return render(request, 'cursos/acessa_aula.html', context)


@login_required
@inscricao_required
def material(request, slug, pk):
    curso = request.curso
    material = get_object_or_404(
        Material,
        pk=pk,
        aula__curso=curso
    )
    aula = material.aula

    if not request.user.is_staff and not aula.is_disponivel():
        messages.error(request, 'Este material não está disponível.')
        redirect('cursos_aulas', slug=curso.slug, pk=aula.pk)

    if not material.is_embedded():
        return redirect(material.arquivo.url)

    context = {
        'curso': curso,
        'aula': aula,
        'material': material,
    }

    return render(request, 'cursos/material.html', context)

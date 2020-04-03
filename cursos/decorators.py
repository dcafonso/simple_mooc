from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Curso, InscricaoCurso


def inscricao_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        curso = get_object_or_404(Curso, slug=slug)
        tem_permissao = request.user.is_staff
        if not tem_permissao:
            try:
                inscricao = InscricaoCurso.objects.get(
                    user=request.user,
                    curso=curso
                )
            except InscricaoCurso.DoesNotExist:
                message = 'Você não tem permissão para acessar esta página!'
            else:
                if inscricao.is_aprovado():
                    tem_permissao = True
                else:
                    message = 'A sua inscrição no curso ainda está pendente!'

        if not tem_permissao:
            messages.error(request, message)
            return redirect('usuarios_dashboard')

        request.curso = curso
        return view_func(request, *args, **kwargs)

    return _wrapper

from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Topicos,
)


class ForumView(ListView):
    paginate_by = 2
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Topicos.objects.all()
        order = self.request.GET.get('order', '')
        if order == 'visualizados':
            queryset = queryset.order_by('-visualizacoes')
        elif order == 'repostas':
            queryset = queryset.order_by('-resposta')

        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Topicos.tags.all()
        return context


class TopicoView(DetailView):
    model = Topicos
    template_name = 'forum/topico.html'

    def get_context_data(self, **kwargs):
        context = super(TopicoView, self).get_context_data(**kwargs)
        context['tags'] = Topicos.tags.all()
        return context


index = ForumView.as_view()
topico = TopicoView.as_view()

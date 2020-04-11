from django.urls import re_path
from .views import (
    index,
    topico,
)


urlpatterns = [
    re_path(r'^$', index, name='forum_index'),
    re_path(r'^tag/(?P<tag>[\w_-]+)/$', index, name='index_tagged'),
    re_path(r'^topico/(?P<slug>[\w_-]+)/$', topico, name='forum_topico'),
]

from django.conf.urls import url, include

from .views import (framework_list,
                    detail, fetch_framework_metadata, add_framework, edit)

app_name = 'frameworks'

urlpatterns = [
    url(r'^$', framework_list, name='list'),
    url(r'^add/$', add_framework, name='add'),
    url(r'^(?P<id>\d+)/$', detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', edit, name='edit'),
    url(r'^(?P<id>\d+)/fetch/$', fetch_framework_metadata, name='fetch_metadata'),
]
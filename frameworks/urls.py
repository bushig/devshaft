from django.conf.urls import url, include

from .views import (framework_list,
                    detail,)

app_name = 'frameworks'

urlpatterns = [
    url(r'^$', framework_list, name='list'),
    url(r'^(?P<pk>\d+)/?', detail, name='detail'),
]
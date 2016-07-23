from django.conf.urls import url, include

from .views import (framework_list,
                    detail,)

urlpatterns = [
    url(r'^$', framework_list, name='list'),
    url(r'^(?P<pk>\d+)/?', detail, name='detail'),
]
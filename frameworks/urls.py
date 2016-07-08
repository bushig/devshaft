from django.conf.urls import url, include

from .views import framework_list

urlpatterns = [
    url(r'^$', framework_list, name='list'),
]
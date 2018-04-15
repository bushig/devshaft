from django.conf.urls import url

from .views import (
    FrameworkList,
    FrameworkLikesCreateView
)

urlpatterns = [
        url(r'^$', FrameworkList.as_view(), name='frameworks-list'),
        url(r'^(?P<id>[\d]+)/likes/$', FrameworkLikesCreateView.as_view(), name='frameworks-likes'),

]
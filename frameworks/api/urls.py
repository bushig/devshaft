from django.conf.urls import url

from .views import (
    FrameworkList,
)

urlpatterns = [
        url(r'^$', FrameworkList.as_view(), name='frameworks-list'),
        ]
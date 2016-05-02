#api version 1

from django.conf.urls import url, include
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets

from assets.api import views as assets_views


urlpatterns = [
    url(r'^assets/$', assets_views.EntryCreateReadView.as_view(), name='assets'),
    url(r'^assets/(?P<id>[\d]+)/$', assets_views.EntryReadUpdateDeleteView.as_view(), name = 'assets'),
    url(r'^assets/(?P<id>[\d]+)/likes/$', assets_views.EntryLikesCreateView.as_view(), name='assets'),
]
from django.conf.urls import url

from .views import (
    EntryListView,
    EntryReadUpdateDeleteView,
    EntryLikesCreateView
)

urlpatterns = [
    url(r'^$', EntryListView.as_view(), name='assets-list'),
    url(r'^(?P<id>[\d]+)/$', EntryReadUpdateDeleteView.as_view(), name = 'assets-crud'),
    url(r'^(?P<id>[\d]+)/likes/$', EntryLikesCreateView.as_view(), name='assets-likes'),
]
from django.conf.urls import url

from .views import (
    EntryListView,
    EntryReadUpdateDeleteView,
)

urlpatterns = [
    url(r'^$', EntryListView.as_view(), name='assets-list'),
    url(r'^(?P<id>[\d]+)/$', EntryReadUpdateDeleteView.as_view(), name = 'assets-crud'),
    #url(r'^/(?P<id>[\d]+)/likes/$', assets_views.EntryLikesCreateView.as_view(), name='assets'),
]
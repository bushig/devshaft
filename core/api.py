#api version 1

from django.conf.urls import url

from assets import views as assets_views


urlpatterns = [
    url(r'^assets/$', assets_views.EntryCreateReadView.as_view(), name='assets'),
    url(r'^assets/(?P<id>[\d]+)/$', assets_views.EntryReadUpdateDeleteView.as_view(), name = 'assets')
]
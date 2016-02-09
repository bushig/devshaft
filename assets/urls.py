from django.conf.urls import url, include

from .views import list, entry_details, add_entry, edit, user_assets, add_version, entry_versions

urlpatterns = [
    url(r'^$', list, name='list'),
    url(r'^(?P<id>[\d]+)/$', entry_details, name='detail'),
    url(r'^add/$', add_entry, name='add_entry'),
    url(r'^(?P<id>[\d]+)/edit/$', edit, name='edit'),
    url(r'^user/(?P<user_id>[\d]+)/$', user_assets, name='user_assets'),
    url(r'^(?P<id>[\d]+)/add$', add_version, name='add_version'),
    url(r'^(?P<id>[\d]+)/versions/$', entry_versions, name='entry_versions'),
]
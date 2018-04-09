from django.conf.urls import url, include

from .views import assets_list, entry_details, add_entry, edit, user_assets, add_version, entry_versions, edit_version, fetch_asset_metadata, revisions_list

app_name = 'assets'

urlpatterns = [
    url(r'^$', assets_list, name='list'),
    url(r'^(?P<id>[\d]+)/$', entry_details, name='detail'),
    url(r'^add/$', add_entry, name='add_entry'),
    url(r'^(?P<id>[\d]+)/edit/$', edit, name='edit'),
    url(r'^user/(?P<user_id>[\d]+)/assets/$', user_assets, name='user_assets'),
    url(r'^(?P<id>[\d]+)/add$', add_version, name='add_version'),
    url(r'^(?P<id>[\d]+)/revisions$', revisions_list, name='revisions_list'),
    url(r'^(?P<id>[\d]+)/versions/$', entry_versions, name='entry_versions'),
    url(r'^(?P<id>[\d]+)/versions/(?P<version_id>[\d]+)/$', edit_version, name='edit_version'),
    url(r'^(?P<id>[\d]+)/fetch/$', fetch_asset_metadata, name='fetch_metadata'),
]
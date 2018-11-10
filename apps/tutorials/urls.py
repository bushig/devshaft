from django.conf.urls import url, include

from .views import tutorial_list, detail, edit, create

app_name = 'tutorials'

urlpatterns = [
    url(r'^$', tutorial_list, name='list'),
    url(r'^(?P<id>[\d]+)/$', detail, name='detail'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>[\d]+)/edit/$', edit, name='edit'),
#     url(r'^user/(?P<user_id>[\d]+)/assets/$', user_assets, name='user_assets'),
#     url(r'^user/(?P<user_id>[\d]+)/likes/$', assets_liked, name='assets_liked'),
#     url(r'^(?P<id>[\d]+)/add$', add_version, name='add_version'),
#     url(r'^(?P<id>[\d]+)/revisions$', revisions_list, name='revisions_list'),
#     url(r'^(?P<id>[\d]+)/versions/$', entry_versions, name='entry_versions'),
#     url(r'^(?P<id>[\d]+)/versions/(?P<version_id>[\d]+)/$', edit_version, name='edit_version'),
#     url(r'^(?P<id>[\d]+)/fetch/$', fetch_asset_metadata, name='fetch_metadata'),
]

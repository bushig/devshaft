from django.conf.urls import url, include

from .views import tutorial_list, detail, edit, create, series_list, series_detail, series_create, series_edit

app_name = 'tutorials'

urlpatterns = [
    url(r'^tutorials/$', tutorial_list, name='list'),
    url(r'^tutorials/(?P<id>[\d]+)/$', detail, name='detail'),
    url(r'^tutorials/create/$', create, name='create'),
    url(r'^tutorials/(?P<id>[\d]+)/edit/$', edit, name='edit'),

    url(r'^series/$', series_list, name='series_list'),
    url(r'^series/(?P<id>[\d]+)/$', series_detail, name='series_detail'),
    url(r'^series/create/$', series_create, name='series_create'),
    url(r'^series/(?P<id>[\d]+)/edit/$', series_edit, name='series_edit'),
#     url(r'^user/(?P<user_id>[\d]+)/assets/$', user_assets, name='user_assets'),
#     url(r'^user/(?P<user_id>[\d]+)/likes/$', assets_liked, name='assets_liked'),
#     url(r'^(?P<id>[\d]+)/add$', add_version, name='add_version'),
#     url(r'^(?P<id>[\d]+)/revisions$', revisions_list, name='revisions_list'),
#     url(r'^(?P<id>[\d]+)/versions/$', entry_versions, name='entry_versions'),
#     url(r'^(?P<id>[\d]+)/versions/(?P<version_id>[\d]+)/$', edit_version, name='edit_version'),
#     url(r'^(?P<id>[\d]+)/fetch/$', fetch_asset_metadata, name='fetch_metadata'),
]

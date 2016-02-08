from django.conf.urls import url, include

from .views import assets_list, assets_entry_details, assets_add_entry, assets_edit, assets_user_assets

urlpatterns = [
    url(r'^$', assets_list, name='assets_list'),
    url(r'^(?P<id>[\d]+)/$', assets_entry_details, name='assets_detail'),
    url(r'^add/$', assets_add_entry, name='assets_add_entry'),
    url(r'^(?P<id>[\d]+)/edit/$', assets_edit, name='assets_edit'),
    url(r'^user/(?P<user_id>[\d]+)/$', assets_user_assets, name='assets_user_assets'),
]
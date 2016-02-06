from django.conf.urls import url, include
from .views import assets_list, assets_entry_details, assets_add_entry

urlpatterns = [
    url(r'^$', assets_list, name='assets_list'),
    url(r'^(?P<id>[\d]+)/$', assets_entry_details, name='assets_detail'),
    url(r'^add/$', assets_add_entry, name='assets_add_entry')
]
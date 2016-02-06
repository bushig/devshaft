from django.conf.urls import url, include
from .views import assets_list
urlpatterns = [
    url(r'^$', assets_list, name='assets_list'),

]
from django.conf.urls import url, include

from .views import main_page

app_name = 'main_page'

urlpatterns = [
    url(r'^$', main_page, name='stats'),
]
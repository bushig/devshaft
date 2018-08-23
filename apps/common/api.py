#api version 1

from django.conf.urls import url, include

app_name = 'api'

urlpatterns = [
    #Assets app
    url(r'^assets/', include('apps.assets.api.urls')),
    #Framework app
    url(r'^frameworks/', include('apps.frameworks.api.urls')),
]
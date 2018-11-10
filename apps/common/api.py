#api version 1

from django.conf.urls import url, include

app_name = 'api'

urlpatterns = [
    url(r'^assets/', include('apps.assets.api.urls')),
    url(r'^frameworks/', include('apps.frameworks.api.urls')),
    url(r'^tutorials/', include('apps.tutorials.api.urls'))
]
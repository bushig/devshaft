#api version 1

from django.conf.urls import url, include



urlpatterns = [
    #Assets app
    url(r'^assets/', include('assets.api.urls')),
    #Framework app
    url(r'^frameworks/', include('frameworks.api.urls')),
]
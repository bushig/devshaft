"""godot_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from assets import urls as assets_urls
from frameworks import urls as frameworks_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^assets/', include(assets_urls, namespace='assets')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^frameworks/', include(frameworks_urls, namespace='frameworks')),
    url(r'^api/', include('common.api', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
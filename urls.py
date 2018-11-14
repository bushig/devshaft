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
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from apps.common.sitemap import sitemaps
from apps.assets import urls as assets_urls
from apps.frameworks import urls as frameworks_urls

urlpatterns = [
    path('octo/', admin.site.urls),
    path('', include('apps.main_page.urls')),
    path('assets/', include('apps.assets.urls')),
    path('accounts/', include('allauth.urls')),
    path('frameworks/', include('apps.frameworks.urls')),
    path('', include('apps.tutorials.urls')),
    path('api/', include('apps.common.api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('markdownx/', include('markdownx.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
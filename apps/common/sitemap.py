from django.contrib.sitemaps import Sitemap
from apps.tutorials.models import Tutorial
from apps.frameworks.models import Framework
from apps.assets.models import Asset

from zinnia.sitemaps import AuthorSitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import TagSitemap

class TutorialSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Tutorial.objects.all()

    def lastmod(self, obj):
        return obj.updated


class FrameworkSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Framework.objects.all()

    def lastmod(self, obj):
        return obj.updated


class AssetsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Asset.objects.all()

    def lastmod(self, obj):
        return obj.updated


sitemaps = {'tutorials': TutorialSitemap, 'frameworks': FrameworkSitemap, 'assets': AssetsSitemap,
            'tags': TagSitemap,
            'blog': EntrySitemap,
            'authors': AuthorSitemap,
            'categories': CategorySitemap
            }

from django.shortcuts import render

from apps.assets.models import Asset
from apps.frameworks.models import Framework
from apps.tutorials.models import Series, Tutorial
from zinnia.models.entry import Entry


def main_page(request):
    news_count = Entry.objects.count()
    assets_count = Asset.objects.count()
    frameworks_count = Framework.objects.count()
    series_count = Series.objects.count()
    tutorials_count = Tutorial.objects.count()
    return render(request, 'main_page.html', {'news_count': news_count, 'assets_count': assets_count,
                                              'frameworks_count': frameworks_count, 'series_count': series_count,
                                              'tutorials_count': tutorials_count
                                              })

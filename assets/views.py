from django.shortcuts import render, get_object_or_404
from .models import Category, Entry, VersionHistory

def assets_list(request):
    entries=Entry.objects.all()
    context={'entries':entries}
    return render(request, 'assets_list.html', context=context)

def assets_entry_details(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry)
    context={'entry':entry, 'versions':versions}
    return render(request, 'assets_detail.html', context)

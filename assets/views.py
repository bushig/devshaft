from django.shortcuts import render
from .models import Categoty, Entry, VersionHistory

def assets_list(request):
    categories=Categoty.objects.all()
    entries=Entry.objects.all()
    context={'categories':categories, 'entries':entries}
    return render(request, 'assets_list.html', context=context)

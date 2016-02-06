from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Entry, VersionHistory
from .forms import EntryForm
from django.contrib import messages

def assets_list(request):
    entries=Entry.objects.all()
    context={'entries':entries}
    return render(request, 'assets_list.html', context=context)

def assets_entry_details(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry).order_by('-timestamp')
    context={'entry':entry, 'versions':versions}
    return render(request, 'assets_detail.html', context)

def assets_add_entry(request):
    form=EntryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfuly created new asset')
        return redirect('assets:assets_list')
    context={'form': form}
    return render(request, 'assets_add_entry.html', context)
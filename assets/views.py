from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from .models import Category, Entry, VersionHistory
from .forms import EntryForm, VersionForm


def list(request):
    entries=Entry.objects.exclude(versionhistory__isnull=True) #Maybe move to Manager?
    context={'entries':entries}
    return render(request, 'assets_list.html', context=context)

def entry_details(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry).order_by('-timestamp')
    context={'entry':entry, 'versions':versions}
    return render(request, 'assets_detail.html', context)

@login_required()
def add_entry(request):
    form=EntryForm(request.POST or None)
    if form.is_valid():
        entry=form.save(commit=False)
        entry.user=request.user
        entry.save()
        messages.success(request, 'Successfuly created new asset')
        return redirect('assets:assets_list')
    context={'form': form}
    return render(request, 'assets_add_entry.html', context)

@login_required()
def add_version(request, id):
    entry=get_object_or_404(Entry, id=id)
    if request.user!=entry.user:
        raise PermissionDenied
    form=VersionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        version=form.save(commit=False)
        version.file=request.FILES['file']
        version.entry=entry
        version.save()
        return redirect('assets:detail', id)
    context={'form': form}
    return render(request, 'assets_add_version.html', context)

def user_assets(request, user_id):
    user=get_object_or_404(User, id=user_id)
    entries=Entry.objects.filter(user=user)
    context={'entries': entries}
    return render(request, 'assets_list.html', context)

def entry_versions(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry)
    context={'entry':entry, 'versions': versions}
    return render(request, 'assets_entry_versions.html', context)

@login_required()
def edit(request, id):
    asset=get_object_or_404(Entry, id=id)
    if request.user==asset.user:
        form=EntryForm(request.POST or None, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset saved')
            return redirect('assets:detail', id)
        context={'form': form}
        return render(request, 'assets_entry_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)

@login_required()
def edit_version(request, id, version_id):
    asset=get_object_or_404(Entry, id=id)
    version=get_object_or_404(VersionHistory, id=version_id)
    if request.user==asset.user:
        form=VersionForm(request.POST or None, instance=version)
        if form.is_valid():
            form.save()
            messages.success(request, 'Version saved')
            return redirect('assets:detail', id)
        context={'form': form}
        return render(request, 'assets_version_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)
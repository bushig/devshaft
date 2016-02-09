from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Category, Entry, VersionHistory
from .forms import EntryForm


def assets_list(request):
    entries=Entry.objects.exclude(versionhistory__isnull=True)
    context={'entries':entries}
    return render(request, 'assets_list.html', context=context)

def assets_entry_details(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry).order_by('-timestamp')
    context={'entry':entry, 'versions':versions}
    return render(request, 'assets_detail.html', context)

@login_required()
def assets_add_entry(request):
    form=EntryForm(request.POST or None)
    if form.is_valid():
        entry=form.save(commit=False)
        entry.user=request.user
        entry.save()
        messages.success(request, 'Successfuly created new asset')
        return redirect('assets:assets_list')
    context={'form': form}
    return render(request, 'assets_add_entry.html', context)

def assets_user_assets(request, user_id):
    user=get_object_or_404(User, id=user_id)
    entries=Entry.objects.filter(user=user)
    context={'entries': entries}
    return render(request, 'assets_list.html', context)

@login_required()
def assets_edit(request, id):
    asset=get_object_or_404(Entry, id=id)
    if request.user==asset.user:
        form=EntryForm(request.POST or None, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved')
            return redirect('assets:assets_list')
        context={'form': form}
        return render(request, 'assets_entry_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:assets_list')
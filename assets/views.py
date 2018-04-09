from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.utils import timezone

import reversion
from reversion.models import Version

from .models import Category, Entry, VersionHistory
from .forms import EntryForm, VersionForm, EntryImageFormSet, VersionFormEdit
from .filters import EntryFilter
from languages.models import Language
from frameworks.models import Framework

def assets_list(request):  # TODO:Move to manager, improve image perform
    filter = EntryFilter(request.GET or None, queryset=Entry.objects.all())
    page = request.GET.get('page')
    paginator = Paginator(filter.qs, 16)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated = paginator.page(paginator.num_pages)

    context = {'entries': paginated, 'filter': filter}
    return render(request, 'assets_list.html', context=context)


def user_assets(request, user_id):  # TODO: Make it DRYer
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        queryset = Entry.objects.filter(user=user)
    else:
        queryset = Entry.objects.filter(user=user)
    filter = EntryFilter(request.GET or None, queryset=queryset)
    page = request.GET.get('page')
    paginator = Paginator(filter.qs, 16)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated = paginator.page(paginator.num_pages)

    context = {'entries': paginated, 'user': user, 'filter': filter}
    return render(request, 'user_assets.html', context)


def entry_details(request, id):
    entry = get_object_or_404(Entry, id=id)
    images = entry.entryimage_set.all()
    versions = VersionHistory.objects.filter(entry=entry)
    context = {'entry': entry, 'versions': versions, 'images': images}
    if request.user.is_authenticated:
        user_liked = entry.liked(request.user)
        context['user_liked'] = user_liked
    return render(request, 'assets_detail.html', context)


@login_required()
def add_entry(request):  # TODO:REFACTOR to display formset
    form = EntryForm(request.POST or None)
    if form.is_valid():
        with reversion.create_revision():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            entry.updated = timezone.now()
            form.save_m2m()

            reversion.set_user(request.user)
            reversion.set_comment("Initial revision")

        if entry.entry_type == 1: # version type
            messages.success(request, 'Successfully created new asset. Now add version.')
            return redirect('assets:add_version', id=entry.id)
        else:
            messages.success(request, 'Successfully created new asset.')
            return redirect('assets:detail', id=entry.id)
    context = {'form': form}
    return render(request, 'assets_add_entry.html', context)


@login_required()
def add_version(request, id):
    entry = get_object_or_404(Entry, id=id)
    if request.user != entry.user or entry.entry_type != 1:
        raise PermissionDenied
    form = VersionForm(request.POST or None, request.FILES or None, initial={'entry': entry})
    if form.is_valid():
        version = form.save(commit=False)
        version.file = request.FILES['file']
        version.entry = entry
        entry.updated = timezone.now()
        version.save()
        return redirect('assets:detail', id)
    context = {'form': form}
    return render(request, 'assets_add_version.html', context)


def entry_versions(request, id):
    entry = get_object_or_404(Entry, id=id)
    versions = VersionHistory.objects.filter(entry=entry)
    context = {'entry': entry, 'versions': versions}
    return render(request, 'assets_entry_versions.html', context)


@login_required()
def edit(request, id):  # TODO: REFACTOR!
    asset = get_object_or_404(Entry, id=id)
    if request.user == asset.user:
        form = EntryForm(request.POST or None, instance=asset)
        formset = EntryImageFormSet(request.POST or None, request.FILES or None, instance=asset)
        if form.is_valid() and formset.is_valid():
            with reversion.create_revision():
                form.save()

                reversion.set_user(request.user)
                reversion.set_comment("Edited by user")

            formset.save()
            messages.success(request, 'Asset saved')
            return redirect('assets:detail', id)
        context = {'form': form, 'formset': formset}
        return render(request, 'assets_entry_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)


@login_required()
def edit_version(request, id, version_id):
    asset = get_object_or_404(Entry, id=id)
    version = get_object_or_404(VersionHistory, id=version_id)
    if request.user == asset.user:
        form = VersionFormEdit(request.POST or None, request.FILES or None, instance=version)
        if form.is_valid():
            form.save()
            messages.success(request, 'Version saved')
            return redirect('assets:detail', id)
        context = {'form': form}
        return render(request, 'assets_version_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)


@login_required()
def fetch_asset_metadata(request, id):
    asset = get_object_or_404(Entry, id=id)
    asset.fetch_metadata()
    return redirect('assets:detail', id)
# TODO: make asset list, user asset list and liked assets CBV

def revisions_list(request, id):
    entry = get_object_or_404(Entry, id=id)
    revisions = Version.objects.get_for_object(entry)
    results = []
    for revision in revisions:
        res = revision.field_dict
        entry = Entry.objects.get(id=id)
        res['category'] = Category.objects.get(id = revision.field_dict['category_id'])
        res['entry_type'] = entry.get_entry_type_display()
        res['languages'] = [Language.objects.get(id=i) for i in revision.field_dict['languages']]
        res['frameworks'] = [Framework.objects.get(id=i) for i in revision.field_dict['frameworks']]
        results.append(res)
    context = {'revisions': results}
    return render(request, 'assets_reversion_list.html', context=context)
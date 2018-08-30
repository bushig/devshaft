from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

import reversion
from reversion.models import Version

from .models import Category, Asset, Release
from .forms import AssetForm, ReleaseForm, EntryImageFormSet, ReleaseFormEdit, ReleaseUploadsFormSet
from .filters import EntryFilter
from apps.languages.models import Language
from apps.frameworks.models import Framework

def assets_list(request):  # TODO:Move to manager, improve image perform
    filter = EntryFilter(request.GET or None, queryset=Asset.objects.all())
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
        queryset = Asset.objects.filter(user=user)
    else:
        queryset = Asset.objects.filter(user=user)
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

def assets_liked(request, user_id):  # TODO: Make it DRYer
    user = get_object_or_404(User, id=user_id)
    queryset = Asset.objects.filter(users_liked=user)
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
    asset = get_object_or_404(Asset, id=id)
    images = asset.images.all()
    versions = Release.objects.filter(asset=asset)
    context = {'entry': asset, 'versions': versions, 'images': images}
    if request.user.is_authenticated:
        user_liked = asset.liked(request.user)
        context['user_liked'] = user_liked
    return render(request, 'assets_detail.html', context)


@login_required()
def add_entry(request):  # TODO:REFACTOR to display formset
    form = AssetForm(request.POST or None)
    if form.is_valid():
        with reversion.create_revision():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            entry.updated = timezone.now()
            form.save_m2m()

            reversion.set_user(request.user)
            reversion.set_comment("Initial revision")

        messages.success(request, 'Successfully created new asset.')
        return redirect('assets:detail', id=entry.id)
    context = {'form': form}
    return render(request, 'assets_add_entry.html', context)


@login_required()
def add_version(request, id):
    entry = get_object_or_404(Asset, id=id)
    if request.user != entry.user:
        raise PermissionDenied
    form = ReleaseForm(request.POST or None, request.FILES or None, initial={'entry': entry})
    formset = ReleaseUploadsFormSet(request.POST or None, request.FILES or None, instance=form.instance)
    if form.is_valid() and formset.is_valid():
        version = form.save(commit=False)
        version.asset = entry
        entry.updated = timezone.now()
        version.save()
        uploads = formset.save(commit=False)
        for upload in uploads:
            upload.release = version
            upload.save()
        messages.success(request, 'Successfuly created release')
        return redirect('assets:detail', id)
    context = {'form': form, 'formset': formset}
    return render(request, 'assets_add_version.html', context)


def entry_versions(request, id):
    entry = get_object_or_404(Asset, id=id)
    versions = Release.objects.filter(asset=entry)
    context = {'entry': entry, 'versions': versions}
    return render(request, 'assets_entry_versions.html', context)


@login_required()
def edit(request, id):  # TODO: REFACTOR!
    asset = get_object_or_404(Asset, id=id)
    if request.user.is_authenticated:
        form = AssetForm(request.POST or None, instance=asset)
        formset = EntryImageFormSet(request.POST or None, request.FILES or None, instance=asset)
        if form.is_valid() and formset.is_valid():
            with reversion.create_revision():
                form.save()

                reversion.set_user(request.user)
                reversion.set_comment("Edited by {}".format(request.user))

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
    asset = get_object_or_404(Asset, id=id)
    version = get_object_or_404(Release, id=version_id)
    if request.user == asset.user:
        form = ReleaseFormEdit(request.POST or None, request.FILES or None, instance=version)
        formset = ReleaseUploadsFormSet(request.POST or None, request.FILES or None, instance=version)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Release saved')
            return redirect('assets:detail', id)
        context = {'form': form, formset: 'formset'}
        return render(request, 'assets_version_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)


@login_required()
def fetch_asset_metadata(request, id):
    asset = get_object_or_404(Asset, id=id)
    asset.fetch_metadata()
    return redirect('assets:detail', id)
# TODO: make asset list, user asset list and liked assets CBV

def revisions_list(request, id):
    asset = get_object_or_404(Asset, id=id)
    revisions = Version.objects.get_for_object(asset)[:50]
    results = []
    for revision in revisions:
        res = revision.field_dict
        res['category'] = Category.objects.get(id = revision.field_dict['category_id'])
        res['languages'] = [Language.objects.get(id=i) for i in revision.field_dict['languages']]
        res['frameworks'] = [Framework.objects.get(id=i) for i in revision.field_dict['frameworks']]
        results.append(res)
    context = {'revisions': results, 'asset': asset}
    return render(request, 'assets_reversion_list.html', context=context)
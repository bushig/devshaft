from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin

from .models import Category, Entry, VersionHistory, EntryImage, EntryLikes
from .forms import EntryForm, VersionForm, EntryImageFormSet, VersionFormEdit, AssetsSearch
from .serializers import EntrySerializer, EntryLikesSerializer
from .permissions import IsOwnerOrReadOnly


def list(request):
    entries=Entry.objects.exclude(versionhistory__isnull=True) #TODO: move to Manager
    search = AssetsSearch(data=request.GET or None)
    context={'entries':entries, 'search': search}
    return render(request, 'assets_list.html', context=context)

def user_assets(request, user_id):
    user=get_object_or_404(User, id=user_id)
    entries=Entry.objects.filter(user=user)
    context={'entries': entries}
    return render(request, 'assets_list.html', context)

def entry_details(request, id):
    entry=get_object_or_404(Entry, id=id)
    images = entry.entryimage_set.all()
    user_liked = entry.liked(request.user)
    versions=VersionHistory.objects.filter(entry=entry)
    context={'entry':entry, 'versions':versions, 'images': images, 'user_liked': user_liked}
    return render(request, 'assets_detail.html', context)

@login_required()
def add_entry(request):  #TODO:REFACTOR to display formset
    form=EntryForm(request.POST or None)
    if form.is_valid():
        entry=form.save(commit=False)
        entry.user=request.user
        entry.save()
        messages.success(request, 'Successfuly created new asset. Now add version')
        entry.refresh_from_db()
        return redirect('assets:add_version', id=entry.id)
    context={'form': form}
    return render(request, 'assets_add_entry.html', context)

@login_required()
def add_version(request, id):
    entry=get_object_or_404(Entry, id=id)
    if request.user!=entry.user:
        raise PermissionDenied
    form=VersionForm(request.POST or None, request.FILES or None, initial={'entry': entry})
    if form.is_valid():
        version=form.save(commit=False)
        version.file=request.FILES['file']
        version.entry=entry
        version.save()
        return redirect('assets:detail', id)
    context={'form': form}
    return render(request, 'assets_add_version.html', context)

def entry_versions(request, id):
    entry=get_object_or_404(Entry, id=id)
    versions=VersionHistory.objects.filter(entry=entry)
    context={'entry':entry, 'versions': versions}
    return render(request, 'assets_entry_versions.html', context)

@login_required()
def edit(request, id):#TODO: REFACTOR!
    asset=get_object_or_404(Entry, id=id)
    if request.user==asset.user:
        form=EntryForm(request.POST or None, instance=asset)
        formset=EntryImageFormSet(request.POST or None, request.FILES or None, instance = asset)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Asset saved')
            return redirect('assets:detail', id)
        context={'form': form, 'formset': formset}
        return render(request, 'assets_entry_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)

@login_required()
def edit_version(request, id, version_id):
    asset=get_object_or_404(Entry, id=id)
    version=get_object_or_404(VersionHistory, id=version_id)
    if request.user==asset.user:
        form=VersionFormEdit(request.POST or None, instance=version)
        if form.is_valid():
            form.save() #TODO:FIX FILE UPLOADING
            messages.success(request, 'Version saved')
            return redirect('assets:detail', id)
        context={'form': form}
        return render(request, 'assets_version_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('assets:detail', id)


#API VIEWS!!!

class EntryCreateReadView(ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

class EntryReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'id'


class EntryLikesCreateView(DestroyModelMixin, CreateAPIView):
    '''
    API to post like if is there is no likes from user for this particular asset(201) and to delete it
    if there was any(204).
    '''

    #TODO: return ammount of likes, asset owner cant like his asset, refactor model to have one to many relation

    queryset = EntryLikes.objects.all()
    serializer_class = EntryLikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry = Entry.objects.get(id = kwargs['id'])
        queryset=EntryLikes.objects.filter(user=request.user, entry = kwargs['id'])

        if queryset.exists():
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer.save(user = request.user, entry = entry)
            return Response(status=status.HTTP_201_CREATED)

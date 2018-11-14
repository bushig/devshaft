from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic.base import TemplateView

import reversion
from reversion.models import Version

from .models import Tutorial, Series
from .forms import TutorialForm, TutorialEditForm, SeriesForm, TutorialFormSet
from .filters import TutorialFilter, SeriesFilter
from apps.languages.models import Language
from apps.frameworks.models import Framework

def tutorial_list(request):  # TODO:Move to manager, improve image perform
    filter = TutorialFilter(request.GET or None, queryset=Tutorial.objects.all(), request=request)
    page = request.GET.get('page')
    paginator = Paginator(filter.qs, 10)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated = paginator.page(paginator.num_pages)

    context = {'tutorials': paginated, 'filter': filter}
    return render(request, 'tutorials/tutorials_list.html', context=context)


def detail(request, id):
    tutorial = get_object_or_404(Tutorial, id=id)
    context = {'tutorial': tutorial}
    return render(request, 'tutorials/detail.html', context)

@login_required()
def create(request):
    form = TutorialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        tutorial = form.save(commit=False)
        tutorial.user = request.user
        tutorial.save()
        form.save_m2m()

        messages.success(request, 'Successfully created tutorial.')
        return redirect('tutorials:detail', id=tutorial.id)
    context = {'form': form}
    return render(request, 'tutorials/create.html', context)

@login_required()
def edit(request, id):
    tutorial = get_object_or_404(Tutorial, id=id)
    if request.user == tutorial.user:
        form = TutorialEditForm(request.POST or None, request.FILES or None, instance=tutorial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutorial saved')
            return redirect('tutorials:detail', id)
        context = {'form': form, 'tutorial': tutorial, 'form_media': form.media}
        return render(request, 'tutorials/edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('tutorials:detail', id)


# SERIES
def series_list(request):
    filter = SeriesFilter(request.GET or None, queryset=Series.objects.all(), request=request)
    page = request.GET.get('page')
    paginator = Paginator(filter.qs, 10)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated = paginator.page(paginator.num_pages)

    context = {'series': paginated, 'filter': filter}
    return render(request, 'tutorials/series_list.html', context=context)


def series_detail(request, id):
    series = get_object_or_404(Series, id=id)
    context = {'series': series, 'tutors': series.tutorials.all().order_by('tutorialmembership__order')}
    return render(request, 'tutorials/series_detail.html', context)


def series_create(request):
    form = SeriesForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        tutorial = form.save(commit=False)
        tutorial.user = request.user
        tutorial.save()
        messages.success(request, 'Successfully created series.')
        return redirect('tutorials:series_detail', id=tutorial.id)
    context = {'form': form}
    return render(request, 'tutorials/series_create.html', context)


@login_required()
def series_edit(request, id):
    series = get_object_or_404(Series, id=id)
    if request.user == series.user:
        form = SeriesForm(request.POST or None, request.FILES or None, instance=series)
        formset = TutorialFormSet(request.POST or None, instance=series)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Series saved')
            return redirect('tutorials:series_detail', id)
        context = {'form': form, 'formset': formset}
        return render(request, 'tutorials/series_edit.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('tutorials:series_detail', id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import reversion
from reversion.models import Version

from .filters import FrameworkFilter
from .models import Framework
from .forms import FrameworkForm, FrameworkImageFormSet, FrameworkEditForm
from .utils import check_framework_equal_to_version

def framework_list(request):
    filter = FrameworkFilter(request.GET or None, queryset=Framework.objects.all())
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
    context = {'frameworks': paginated, 'filter': filter}
    return render(request, 'frameworks/list.html', context)

def detail(request, id):
    framework = Framework.objects.get(id=id)
    images = framework.frameworkimage_set.all()
    context = {'framework': framework, 'images': images}
    return render(request, 'frameworks/detail.html', context)

def add_framework(request):  # TODO:REFACTOR to display formset
    form = FrameworkForm(request.POST or None)
    if form.is_valid():
        framework = form.save(commit=False)
        framework.user = request.user
        framework.save()
        form.save_m2m()

        messages.success(request, 'Successfully created new framework.')
        return redirect('frameworks:detail', id=framework.id)
    context = {'form': form}
    return render(request, 'frameworks/create_framework.html', context)

@login_required()
def edit(request, id):  # TODO: REFACTOR!
    framework = get_object_or_404(Framework, id=id)
    if request.user == framework.user:
        form = FrameworkEditForm(request.POST or None, instance=framework)
        formset = FrameworkImageFormSet(request.POST or None, request.FILES or None, instance=framework)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Framework saved')
            return redirect('frameworks:detail', id)
        context = {'form': form, 'formset': formset, 'framework': framework}
        return render(request, 'frameworks/edit_framework.html', context)
    else:
        messages.warning(request, "You can't edit this one.")
        return redirect('frameworks:detail', id)


@login_required()
def fetch_framework_metadata(request, id):
    framework = get_object_or_404(Framework, id=id)
    framework.fetch_metadata()
    return redirect('frameworks:detail', id)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

import reversion
from reversion.models import Version

from .models import Tutorial
# from .forms import AssetForm, ReleaseForm, EntryImageFormSet, ReleaseFormEdit, ReleaseUploadsFormSet
from .filters import TutorialFilter
from apps.languages.models import Language
from apps.frameworks.models import Framework

def tutorial_list(request):  # TODO:Move to manager, improve image perform
    filter = TutorialFilter(request.GET or None, queryset=Tutorial.objects.all())
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

    context = {'tutorials': paginated, 'filter': filter}
    return render(request, 'tutorials/tutorials_list.html', context=context)
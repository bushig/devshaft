from django.shortcuts import render
from .models import Categoty

def assets_list(request):
    categories=Categoty.objects.all()
    context={'categories':categories}
    return render(request, 'assets_list.html', context=context)

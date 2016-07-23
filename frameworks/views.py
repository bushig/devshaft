from django.shortcuts import render

from .models import Framework


def framework_list(request):
    return render(request, 'framework_list.html')

def detail(request, pk):
    framework = Framework.objects.get(pk=pk)
    context = {'framework': framework}
    return render(request, 'framework_detail.html', context)
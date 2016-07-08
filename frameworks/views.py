from django.shortcuts import render


def framework_list(request):
    return render(request, 'framework_list.html')

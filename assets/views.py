from django.shortcuts import render

def assets_list(request):
    return render(request, 'assets_list.html')

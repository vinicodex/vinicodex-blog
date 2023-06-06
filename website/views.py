from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html')

def projects(request):
    return render(request, 'website/projects.html')


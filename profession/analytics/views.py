from django.shortcuts import render


def index(request):
    return render(request, 'analytics/index.html')


def demand(request):
    return render(request, 'analytics/demand.html')


def geography(request):
    return render(request, 'analytics/geography.html')


def skills(request):
    return render(request, 'analytics/skills.html')


def recent(request):
    return render(request, 'analytics/recent.html')

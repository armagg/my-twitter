from django.contrib.auth.models import User
from django.shortcuts import render

from paging.models import Page


def homepage(request):
    users = User.objects.all()
    channels = Page.objects.filter(personal_page=False)
    return render(request, 'home.html', {'users': users, 'channels': channels})


def new(request):
    print(request.POST.get('data'))
    if request.POST:
        print(request.POST)
    return render(request, 'home.html')

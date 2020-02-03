from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


def new(request):
    print(request.POST.get('data'))
    if request.POST:
        print(request.POST)
    return render(request, 'home.html')


def list(request):
    return render(request, 'commentList/list.html', {'numbers': [None] * 10})

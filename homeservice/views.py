from django.shortcuts import render


# Create your views here.
def homepage(request):
    return render(request, 'home.html')


def new(request):
    print(request.POST.get('data'))
    if request.POST:
        print(request.POST)
    return render(request, 'home.html')

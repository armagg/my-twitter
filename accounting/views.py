from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounting.forms import UserForm, AccountForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'accounting/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        # account_form = AccountForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # account = account_form.save(commit=False)
            # account.user = user
            # account.save()
            registered = True
            # redirect('index')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        account_form = AccountForm()
    return render(request, 'accounting/signup.html',
                  {'user_form': user_form,
                   # 'account_form': account_form,
                   'registered': registered})


def login(request):
    print(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            return HttpResponseRedirect(reverse('index'))
            # if user.is_active:
            #     login(request, user)
            #     return HttpResponseRedirect(reverse('index'))
            # else:
            #     return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'accounting/login.html', {})

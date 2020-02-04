import json
from http.client import HTTPResponse

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from django.utils.html import strip_tags

from following.models import Follow
from paging.models import Page
from .forms import SignUpForm
from .models import Token, create_new_token, Account
from homeservice.views import homepage


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            if user.is_active:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'home.html')
                else:
                    errors = {
                        'password': 'incorrect password'
                    }
            else:
                errors = {
                    'authentication': 'check your email to activate your account!'
                }
        else:
            errors = {
                'invalid_user': "Invalid login details given"
            }
    else:
        errors = {}
    return render(request, 'accounting/login.html', {'errors': json.dumps(errors)})


def activate(request, username, code):
    token = Token.objects.filter(username=username, code=code).first()
    if token is not None:
        user = User.objects.filter(username=username).first()
        user.is_active = True
        user.save()

        account = Account(user=user)
        account.user = user
        account.name = str(user.username)
        account.save()

        personal_page = Page(personal_page=True, title=user.username + ' page', creator=account,
                             page_id=account.user.username)
        personal_page.save()
        personal_page.admins.add(account)
        personal_page.save()

        token.delete()
        return render(request, 'accounting/activate_done.html')
    else:
        errors = {
            'token': 'invalid token code for activation'
        }
        return render(request, 'accounting/login.html', {'errors': json.dumps(errors)})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            token = create_new_token(username=user.username)
            token.save()
            data = {
                'user': user,
                'domain': current_site.domain,
                'token': token.code,
            }
            message = render_to_string('accounting/activation_page.html', data)
            text_content = strip_tags(message)
            to_email = form.cleaned_data.get('email')
            # send_mail(mail_subject, text_content, 'joorabnakhi@gmail.com', [to_email])
            return render(request, 'accounting/activation_page.html', data)

            return render(request, 'accounting/activation_sent.html')
        else:
            return render(request, 'accounting/signup.html', {'form': form, 'errors': json.dumps(form.errors)})
    else:
        form = SignUpForm()
        return render(request, 'accounting/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/home')


def get_profile_page(request, owner):
    setting = request.user == owner
    followed = False
    if Follow.objects.filter(followed=owner.account, follower=request.user.account):
        followed = True
    return render(request, 'accounting/profile.html', {'owner': owner, 'setting': setting, 'followed': followed})


@login_required
def my_profile(request):
    return get_profile_page(request, request.user)

@login_required
def profile(request, username):
    owner = User.objects.filter(username=username).first()
    if owner:
        return get_profile_page(request, owner)
    else:
        return HttpResponse(status=404)


def forget_password_view(request):
    return render(request, 'accounting/forgot_password.html')


def reset_password_view(request):
    return render(request, 'accounting/reset_password.html')


@login_required
def edit_profile(request):
    print(request.user.account.profile_photo.url)
    errors = []
    if request.POST:
        if request.FILES:
            try:
                request.user.account.profile_photo = request.FILES.get('profile_photo')
                request.user.account.save()
            except:
                errors.append('cant load image!')

        try:
            username = request.POST.get('username')
            name = request.POST.get('name')
            email = request.POST.get('email')
            location = request.POST.get('location')
            bio = request.POST.get('bio')
        except:
            errors.append('bad format of data')
        if username:
            if str(request.user.username) is not str(username):
                if User.objects.filter(username=username):
                    errors.append('this username is token by others ...')
                else:
                    page = Page.objects.get(page_id=request.user.username)
                    page.page_id = username
                    page.save()
                    request.user.username = username
                    request.user.save()

        if location:
            request.user.account.location = location
        if bio:
            request.user.account.bio = bio
        if email:
            request.user.email = email
        if name:
            request.user.account.name = name

        request.user.save()
        request.user.account.save()
    return render(request, 'accounting/profile_edit.html', {'errors': json.dumps(errors)})

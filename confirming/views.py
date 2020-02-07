from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from accounting.models import Account
from confirming.models import ConfirmRequest
from following.models import FollowPage, Follow
from paging.models import Page


@csrf_exempt
@login_required
def follow_page_request(request, page_id):
    q = Page.objects.filter(page_id=page_id)
    if not q.exists():
        return HttpResponse(status=404)
    page = q.get()
    follower = request.user.account
    q = FollowPage.objects.filter(followed=page, follower=follower)
    if q.exists():
        q.delete()
        if page.personal_page:
            Follow.objects.filter(follower=follower, followed=page.creator).delete()
    else:
        if page.public:
            if page.personal_page:
                follow = Follow(follower=follower, followed=page.creator)
                follow.save()
            follow = FollowPage(follower=follower, followed=page)
            follow.save()
        else:
            confirm = ConfirmRequest(channel=page, account=request.user.account)
            confirm.save()
    if page.personal_page:
        return redirect('accounting:profile', page_id)
    return redirect('channelling:channel', page_id)


@login_required
def confirm(request, page_id, username):
    q = Page.objects.filter(page_id=page_id)
    if not q.exists():
        return HttpResponse(status=404)
    page = q.get()

    if not page.is_this_admin(request.user.account):
        return HttpResponse(status=404)

    q = User.objects.filter(username=username)
    if not q.exists():
        return HttpResponse(status=404)
    account = Account.objects.filter(user__username=username).get()

    q = ConfirmRequest.objects.filter(account=account, channel=page)
    if not q.exists():
        return HttpResponse(status=404)

    q.delete()
    follow = FollowPage(follower=account, followed=page)
    follow.save()
    if page.personal_page:
        follow = Follow(follower=account, followed=page.creator)
        follow.save()

    if page.personal_page:
        return redirect('accounting:profile', page_id)
    return redirect('channelling:channel', page_id)


def decline(request, page_id, username):
    q = Page.objects.filter(page_id=page_id)
    if not q.exists():
        return HttpResponse(status=404)
    page = q.get()

    if not page.is_this_admin(request.user.account):
        return HttpResponse(status=404)

    q = User.objects.filter(username=username)
    if not q.exists():
        return HttpResponse(status=404)
    account = Account.objects.filter(user__username=username).get()

    q = ConfirmRequest.objects.filter(account=account, channel=page)
    if not q.exists():
        return HttpResponse(status=404)
    q.delete()
    if page.personal_page:
        return redirect('accounting:profile', page_id)
    return redirect('channelling:channel', page_id)

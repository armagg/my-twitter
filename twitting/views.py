import copy
import json
import html2text


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from accounting.models import Account
from paging.models import Page
from paging.views import page
from searchengine.models import DocIndex
from twitting.models import Tweet


@login_required
def new_post(request):
    if request.POST:
        content = request.POST.get('content')
        if not Page.objects.filter(page_id=request.POST.get('page_id')):
            return HttpResponse(status=404)
        page = Page.objects.get(page_id=request.POST.get('page_id'))
        admins = page.admins.all()
        is_admin = False
        print('1')
        for admin in admins:
            if admin.id is request.user.account.id:
                is_admin = True
                break
        if not is_admin:
            return HttpResponse(status=404)
        plain_text = html2text.html2text(content)
        tweet = Tweet(document=content, plain_text=plain_text, author=request.user.account, parent_tweet=None,
                      page=page)
        tweet.save()

        DocIndex.add_doc(plain_text, tweet.id, 'tweet')

        return HttpResponse('success', status=200)
    return HttpResponse(status=404)



@login_required
def reply(request):
    if request.POST:
        try:
            username = request.user.username
            content = request.POST.get('content')
            post_id = int(request.POST.get('post_id')[5:])
            parent_tweet = Tweet.objects.get(id=post_id)
            acc = Account.objects.get(user__username=username)
            tweet = Tweet(author=acc, document=content, parent_tweet=parent_tweet,
                          page=parent_tweet.page)
            tweet.save()
            return HttpResponse('success', status=200)
        except Exception as e:
            print(e)
            return HttpResponse('failed', status=400)


@login_required
def edit(request):
    if request.POST:
        try:
            username = request.user.username
            document = request.POST.get('content')
            post_id = int(request.POST.get('post_id')[5:])
            acc = Account.objects.get(user__username=username)
            tweet = Tweet.objects.get(Q(id=post_id))
            if acc.user.username != username:
                return HttpResponse('access denied', status=403)
            tweet.document = document
            tweet.save()
            return HttpResponse('success', status=200)
        except Exception as e:
            print(e)
            return HttpResponse('failed', status=400)


@login_required
def delete(request):
    if request.POST:
        username = request.user.username
        post_id = int(request.POST.get('post_id')[5:])
        tweet = Tweet.objects.get(Q(id=post_id))
        if tweet.get_username() != username:
            return HttpResponse('access denied', status=403)
        tweet.delete()

    return HttpResponse('success', status=200)

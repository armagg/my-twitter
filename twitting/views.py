import copy
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from accounting.models import Account
from paging.models import Page
from twitting.models import Tweet


def comments(request):
    author = {
        'name': 'mmd',
        'avatar': 'https://avatars2.githubusercontent.com/u/45905632?s=460&v=4',
        'state': 'noobe sag',
    }
    # extra avatar
    # http://i9.photobucket.com/albums/a88/creaticode/avatar_2_zps7de12f8b.jpg
    comment1 = {
        'bookmark_state': True,
        'editable': True,
        'like_pack': {
            'like_numbers': 10
        }, 'author': author,
        'content':
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit omnis animi et iure. laudantium vitae, praesentium optio, sapiente distinctio illo?',
        'time': 'hace 20 minutos',
        'replys': [],
        'id': 1,
    }
    comment2 = {
        'bookmark_state': False,
        'like_pack': {
            'like_numbers': 10
        },
        'editable': True,
        'author': author,
        'content':
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit omnis animi et iure. laudantium vitae, praesentium optio, sapiente distinctio illo?',
        'time': 'hace 20 minutos',
        'replys': [comment1, copy.deepcopy(comment1)],
        'id': 2
    }

    comments = list()
    for i in range(10):
        comments.append(copy.deepcopy(comment2))
    i = 0
    for comment in comments:
        comment['id'] = 'tweet' + str(i)
        i += 1
        for reply in comment['replys']:
            reply['id'] = 'tweet' + str(i)
            i += 1
    data = {'comments': comments, 'comments_json': json.dumps(comments), 'tittle': 'mmd pge',
            'can_write': True}
    return render(request, './twitting/commentsPage.html', data)


@login_required
def new_post(request):
    print('new post')
    if request.POST:
        content = request.POST.get('content')
        personal_page = Page.objects.filter(Q(creator=request.user.account) & Q(personal_page=True)).first()
        tweet = Tweet(document=content, author=request.user.account, parent_tweet=None, page=personal_page)
        tweet.save()
    return HttpResponse('success', status=200)


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


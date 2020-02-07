from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from following.models import Follow, FollowPage
from paging.models import Page
from twitting.views import new_post


@csrf_exempt
@login_required
def follow_user_request(request, username):
    followed_username = username
    if not followed_username:
        return HttpResponse(status=404)
    followed = User.objects.get(username=followed_username).account
    follower = request.user.account
    q = Follow.objects.filter(followed=followed, follower=follower)
    if q.exists():
        q.delete()
    else:
        follow = Follow(follower=follower, followed=followed)
        follow.save()
    return redirect('accounting:profile', username)

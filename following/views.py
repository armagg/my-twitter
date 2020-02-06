from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from following.models import Follow, FollowPage
from paging.models import Page
from twitting.views import new_post


@csrf_exempt
@login_required
def follow_user_request(request):
    if request.POST:
        followed_username = request.POST.get('username')
        if not followed_username:
            return HttpResponse(status=404)
        followed = User.objects.get(username=followed_username).account
        follower = request.user.account
        q = Follow.objects.filter(followed=followed, follower=follower)
        if q.exist():
            q.delete()
        else:
            follow = Follow(follower=follower, followed=followed)
            follow.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


@csrf_exempt
@login_required
def follow_page_request(request):
    if request.POST:
        q = Page.objects.filter(page_id=request.POST.get('page_id'))
        if not q.exist():
            return HttpResponse(status=404)
        page = q.get()
        follower = request.user.account
        q = FollowPage.objects.filter(followed=page, follower=follower)
        if q.exist():
            q.delete()
        else:
            follow = FollowPage(follower=follower, followed=page)
            follow.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)

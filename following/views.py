from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from following.models import Follow, FollowPage
from paging.models import Page


@csrf_exempt
@login_required
def follow_request(request):
    if request.POST:
        followed = User.objects.get(username=request.POST.get('username')).account
        follower = request.user.account
        if Follow.objects.filter(followed=followed, follower=follower):
            Follow.objects.get(followed=followed, follower=follower).delete()
        else:
            follow = Follow(follower=follower, followed=followed)
            follow.save()
    return HttpResponse(status=200)


@csrf_exempt
@login_required
def follow_page_request(request):
    if request.POST:
        page = Page.objects.get(page_id=request.POST.get('page_id'))
        follower = request.user.account
        if FollowPage.objects.filter(followed=page, follower=follower):
            FollowPage.objects.get(followed=page, follower=follower).delete()
        else:
            follow = FollowPage(follower=follower, followed=page)
            follow.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from following.models import Follow


@csrf_exempt
@login_required
def follow_request(request):
    if request.POST:
        followed = User.objects.get(username=request.POST.get('username')).account
        follower = request.user.account
        if Follow.objects.filter(followed=followed, follower=follower):
            Follow.objects.get(followed=followed, follower=follower).delete()
        else:
            Follow.objects.create(follower=follower, followed=followed)
    return HttpResponse(status=200)

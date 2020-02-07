from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from liking.models import Like, Dislike
from twitting.models import Tweet


@login_required
def like(request):
    if request.POST:
        try:
            account = request.user.account
            tweet_id = int(request.POST.get('post_id')[5:])
            tweet = Tweet.objects.get(id=tweet_id)
            q = Like.objects.filter(liker=account, tweet_id=tweet_id)
            if q.exists():
                q.get().delete()
            else:
                Like.objects.create(liker=account, tweet=tweet)
            tweet.update_like_number()
            print(tweet.last_like_number)
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
    return HttpResponse(status=404)


@login_required
def dislike(request):
    if request.POST:
        try:
            account = request.user.account
            tweet_id = int(request.POST.get('post_id')[5:])
            tweet = Tweet.objects.get(id=tweet_id)
            q = Dislike.objects.filter(disliker=account, tweet_id=tweet_id)
            if q.exists():
                q.delete()
            else:
                Dislike.objects.create(disliker=account, tweet_id=tweet_id)
            tweet.update_like_number()
            print(tweet.last_like_number)
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
    return HttpResponse(status=404)

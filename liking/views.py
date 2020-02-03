from django.http import HttpResponse

from liking.models import Like, Dislike
from twitting.models import Tweet


def like(request):
    if request.POST:
        try:
            account = request.user.account
            tweet_id = int(request.POST.get('post_id')[5:])
            if Like.has_liked(account.user_id, tweet_id):
                return HttpResponse('you liked this before!', status=400)
            like_post = Like(liker=account, tweet=Tweet.objects.get(tweet_id=tweet_id))
            like_post.save()
            return HttpResponse('liked!', status=200)
        except Exception as e:
            print(e)
            return HttpResponse('some wow exception happened!!', status=501)


def dislike(request):
    if request.POST:
        try:
            account = request.user.account
            tweet_id = int(request.POST.get('post_id')[5:])
            if Dislike.has_disliked(account.user_id, tweet_id):
                return HttpResponse('you disliked this before!', status=400)
            like_post = Like(liker=account, tweet=Tweet.objects.get(tweet_id=tweet_id))
            like_post.save()
            return HttpResponse('disliked', status=200)
        except Exception as e:
            print(e)
            return HttpResponse('some wow exception happened!!', status=501)


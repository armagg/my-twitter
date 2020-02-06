import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from following.models import FollowPage
from paging.models import Page
from searchengine.models import DocIndex


@login_required
def new_channel(request):
    errors = []
    if request.POST:
        id = request.POST.get('id')
        title = request.POST.get('title')
        private = request.POST.get('private')
        description = request.POST.get('description')
        if Page.objects.filter(page_id=id).exist():
            errors.append('this id is token by others...')
        else:
            page = Page(title=title, page_id=id, description=description, personal_page=False,
                        creator=request.user.account)
            page.save()
            page.admins.add(request.user.account)
            page.save()

            DocIndex.add_doc(title, page.page_id, 'page')
            DocIndex.add_doc(description, page.page_id, 'page')

            return redirect('channelling:channel', page.page_id)
    return render(request, 'channelling/new_channeling.html', {'errors': json.dumps(errors)})


def channel_view(request, page_id):
    q = Page.objects.filter(page_id=page_id)
    if q.exist():
        channel = q.get()
        admins = channel.admins.all()
        is_admin = False
        for admin in admins:
            if admin.id is request.user.account.id:
                is_admin = True
                break

        followed = False
        if request.user and request.user.is_authenticated:
            if FollowPage.objects.filter(follower=request.user.account, followed__page_id=page_id):
                followed = True
        data = {'channel': channel, 'admins': admins, 'is_admin': is_admin, 'page_id': channel.page_id,
                'followed': followed}
        return render(request, 'channelling/channel.html', data)
    else:
        return HttpResponse(status=404)


@login_required
def edit_chanel(request, page_id):
    if request.POST:
        Page.objects.filter(page_id=page_id)
        if not q.exist():
            return HttpResponse(status=404)
        page = q.get()

        if not page.is_this_admin(request.user.account.id):
            return HttpResponse(starus=404)

        title = request.POST.get('title')
        description = request.POST.get('description')
        page.update(description=description, title=title)
        page.save()
        return channel_view(request, page_id)
    return HttpResponse(status=404)


@login_required()
def add_admin(request, page_id):
    if request.POST:
        username = request.POST.get('username')
        page = Page.objects.get(page_id=page_id)
        if page.creator.id is not request.user.account.id:
            return HttpResponse(status=404)
        if not User.objects.filter(username=username):
            return redirect('channelling:channel', page_id)
        user = User.objects.get(username=username)
        page.admins.add(user.account)
        return redirect('channelling:channel', page_id)
    else:
        return HttpResponse(status=404)


@login_required()
def remove_admin(request, page_id):
    if request.POST:
        username = request.POST.get('username')
        page = Page.objects.get(page_id=page_id)
        if page.creator.id is not request.user.account.id:
            return HttpResponse(status=404)
        if not User.objects.filter(username=username):
            return redirect('channelling:channel', page_id)
        user = User.objects.get(username=username)
        page.admins.remove(user.account)
        return redirect('channelling:channel', page_id)
    else:
        return HttpResponse(status=404)
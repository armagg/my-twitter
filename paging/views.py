import copy
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from paging.models import Page


@login_required
def my_page(request):
    author = {
        'name': request.user.username,
        'avatar': 'https://avatars2.githubusercontent.com/u/45905632?s=460&v=4',
    }

    # personal_page = Page

    comment = {
        'bookmark_state': False,
        'like_pack': {
            'like_numbers': 10
        },
        'editable': True,
        'author': author,
        'content':
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit omnis animi et iure. laudantium vitae, praesentium optio, sapiente distinctio illo?',
        'time': 'hace 20 minutos',
        'replys': [],
        'id': 2
    }

    comments = list()
    for i in range(3):
        comments.append(copy.deepcopy(comment))
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

# def send_new_post(request):

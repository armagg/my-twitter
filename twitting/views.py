import copy
import json

from django.shortcuts import render


# Create your views here.
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
        comment['id'] = 'a' + str(i)
        i += 1
        for reply in comment['replys']:
            reply['id'] = 'a' + str(i)
            i += 1
    return render(request, './twitting/commentsPage.html',
                  {'comments': comments, 'j': json.dumps(comments), 'tittle': 'mmd pge',
                   'can_write': True})


def my_page(request):
    return render(request, 'twitting/commentsPage.html')

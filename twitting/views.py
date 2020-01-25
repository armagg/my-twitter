from django.shortcuts import render


# Create your views here.
def comments(request):
    author = {
        'name': 'mmd',
        'avatar': 'http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg',
        'state': 'noobe sag',
    }
    # extra avatar
    # http://i9.photobucket.com/albums/a88/creaticode/avatar_2_zps7de12f8b.jpg
    comment1 = {
        'author': author,
        'content':
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit omnis animi et iure. laudantium vitae, praesentium optio, sapiente distinctio illo?',
        'time': 'hace 20 minutos',
        'replys': []
    }
    comment2 = {
        'author': author,
        'content':
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit omnis animi et iure. laudantium vitae, praesentium optio, sapiente distinctio illo?',
        'time': 'hace 20 minutos',
        'replys': [comment1]
    }
    comments = [comment2] * 10
    return render(request, './twitting/commentsPage.html', {'comments': comments, 'tittle': 'mmd pge'})

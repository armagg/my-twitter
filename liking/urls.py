from django.conf.urls import url
from django.urls import path

from liking import views

app_name = 'liking'

urlpatterns = [
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike')
]

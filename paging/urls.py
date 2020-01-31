from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from paging import views

urlpatterns = [
    url(r'^mypage/$', views.my_page, name='mypage')
]

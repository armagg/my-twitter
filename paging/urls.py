from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from paging import views

urlpatterns = [
    url(r'^page/<str:page_id>$', views, name='view_page')
]

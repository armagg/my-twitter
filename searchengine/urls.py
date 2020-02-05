from django.urls import path
from django.conf.urls import url, include

app_name = 'searchengin'

from searchengine import views

urlpatterns = [
    path('', views.search, name='search')
]

from django.conf.urls import url, include
from django.urls import path

from following import views

urlpatterns = [
    path('follow/', views.follow_request, name='follow'),
]

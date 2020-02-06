from django.conf.urls import url, include
from django.urls import path

from following import views

urlpatterns = [
    path('follow/', views.follow_user_request, name='follow'),
    path('follow-page/', views.follow_page_request, name='follow-page'),
]

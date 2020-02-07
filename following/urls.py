from django.urls import path

from following import views

urlpatterns = [
    path('follow/<str:username>', views.follow_user_request, name='follow'),
]


from django.urls import path

from confirming import views

urlpatterns = [
    path('confirm/<str:page_id>/<str:username>', views.confirm, name='confirm'),
    path('decline/<str:page_id>/<str:username>', views.decline, name='decline'),
    path('follow-page/<str:page_id>', views.follow_page_request, name='follow-page'),
]

from django.conf.urls import url, include
from django.urls import path

from paging import views

urlpatterns = [
    path('page/<str:page_id>', views.page, name='view_page'),
    path('my-page', views.my_page, name='my_page')
]

from django.conf.urls import url
from django.urls import path
from homeservice import views

urlpatterns = [
    url(r'^new', views.new, name='new'),
    url('', views.homepage, name='home'),
]

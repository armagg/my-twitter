from django.conf.urls import url
from homeservice import views

app_name = 'homeservice'

urlpatterns = [
    url(r'^list/', views.list, name='list'),
    url('', views.homepage, name='home'),
]

from django.conf.urls import url
from homeservice import views

app_name = 'homeservice'

urlpatterns = [
    url('', views.homepage, name='home'),
]

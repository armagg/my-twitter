# account/urls.py
from django.conf.urls import url
from twitting import views

# SET THE NAMESPACE!
app_name = 'accounting'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^comments/$', views.comments, name='comments'),
]

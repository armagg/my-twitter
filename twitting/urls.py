# account/urls.py
from django.conf.urls import url
from twitting import views

# SET THE NAMESPACE!
app_name = 'twitting'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^comments/$', views.comments, name='comments'),
    url(r'^newpost/$', views.new_post, name='newpost'),
    url(r'^reply/$', views.reply, name='newpost'),
    url(r'^edit/$', views.edit, name='newpost'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^my/$', views.mypage, name='my'),
]

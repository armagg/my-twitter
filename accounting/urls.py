# account/urls.py
from django.conf.urls import url
from django.urls import path

from accounting import views


app_name = 'accounting'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    path('activate/<str:username>/<str:code>', views.activate, name='activate'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^edit/$', views.edit_view, name='edit'),
    url(r'^profile/$', views.profile, name='profile')
]

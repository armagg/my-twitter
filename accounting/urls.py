# account/urls.py
from django.conf.urls import url
from accounting import views

# SET THE NAMESPACE!
app_name = 'accounting'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
]

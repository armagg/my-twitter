from django.conf.urls import url

from alerting import views

app_name = 'alerting'

urlpatterns = [
    url(r'^notifies/', views.notifies, name= 'notifies')
]
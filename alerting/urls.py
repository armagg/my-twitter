from django.conf.urls import url
from django.urls import path

from alerting import views

app_name = 'alerting'

urlpatterns = [
    url(r'^notifies/', views.notifies, name='notifies'),
    path('seen/<int:id>', views.seen_alert, name='seen')
]

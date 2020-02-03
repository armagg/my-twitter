from django.conf.urls import url

from alerting import views

app_name = 'alerting'

urlpatterns = [
    url(r'^get_alerts/', views.get_alerts, name='get_alerts'),
]
# account/urls.py
from django.conf.urls import url
from django.urls import path

from channelling import views

app_name = 'channelling'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^new-channel/', views.new_channel, name='new-channel'),
    path(r'edit-channel/<str:page_id>', views.edit_chanel, name='edit-channel'),
    path('channel/<str:page_id>', views.channel_view, name='channel'),
    path('add-admin/<str:page_id>', views.add_admin, name='add-admin'),
    path('remove-admin/<str:page_id>', views.remove_admin, name='remove-admin'),

]

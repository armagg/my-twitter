#
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path
# from accounting import views
#
# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('sign_up/', views.sign_up, name='sign_up'),
#     path('admin/', admin.site.urls),
#     path('', views.sign_up),
# ]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from accounting import views
app_name = 'Main'

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^index/$', views.index, name='index'),
    # url(r'^special/', views.special, name='special'),
    url(r'^accounting/', include('accounting.urls')),
    url(r'^twitting/', include('twitting.urls')),
    url(r'^paging/', include('paging.urls')),
    url(r'^home/', include('homeservice.urls')),
]

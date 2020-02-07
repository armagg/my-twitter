from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

app_name = 'Main'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # url(r'^index/$', views.index, name='index'),
                  # url(r'^special/', views.special, name='special'),
                  url(r'^accounting/', include('accounting.urls')),
                  url(r'^twitting/', include('twitting.urls')),
                  url(r'^paging/', include('paging.urls')),
                  url(r'^froalaImage/', include('froalaImaging.urls')),
                  url(r'^home/', include('homeservice.urls')),
                  url(r'^liking/', include('liking.urls')),
                  url(r'^following/', include('following.urls')),
                  url(r'^channeling/', include('channelling.urls')),
                  url(r'^alerting/', include('alerting.urls')),
                  url(r'^seach/', include('searchengine.urls')),
                  url(r'^confirming/', include('confirming.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)

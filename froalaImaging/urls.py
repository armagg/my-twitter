from django.conf.urls import url
from froalaImaging import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r"^$", views.index, name="index"),
                  url(r"^upload_image$", views.file_upload, name="upload_image"),
                  url(r"^upload_image_validation", views.upload_image_validation, name="upload_image_validation"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_DIR) + static(settings.STATIC_PUBLIC_URL,
                                                                                          document_root=settings.STATIC_PUBLIC_DIR)

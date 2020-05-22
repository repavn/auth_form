from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from custom_auth.views import UserView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view),
    path('', UserView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

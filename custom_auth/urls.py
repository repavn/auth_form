from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from custom_auth.views import UserView, logout_view, google_login, google_auth_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view),
    path('policy/', TemplateView.as_view(template_name="policy.html"), name='policy'),
    path('terms/', TemplateView.as_view(template_name="terms.html"), name='terms'),
    path('google_login/', google_login),
    path('google_auth_redirect/', google_auth_redirect),
    path('', UserView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

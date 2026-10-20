from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from core import urls as core_urls
from django_user import urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import login_api
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_api),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
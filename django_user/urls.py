from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
#from django.contrib.auth import views
from core import urls as core_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.core.mail import send_mail, BadHeaderError
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new
from django.views.static import serve #new
from django.urls import path, include, re_path #new
from core.views import Signup, PasswordResetAPIView, PasswordResetConfirmAPIView, ChangePasswordAPIView, HomeApi
from core import views





urlpatterns = [
    #path('__debug__/', include('debug_toolbar.urls')),
    path('', include('django.contrib.auth.urls')),
    path('api/login/', views.login_api),
    path('HomeApi/',HomeApi.as_view(),),
    path('', include('core.urls')),
    path('donationdetail/',views.donationdetail,name='donationdetail'),
    path('imageupload/',views.imageupload,name='imageupload'),
    path('api/password-reset/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/reset-password/', views.PasswordResetConfirmAPIView.as_view(), name='reset-password'),
    path('api/change-password/',views.ChangePasswordAPIView.as_view(),),
    path('signup/',Signup.as_view(),name='Signup'),
    path("sendotp_api/",views.sendotp_api,name="sendotp_api"),
    path("update_profile_api/",views.update_profile_api),
    path("profile_api/", views.profile_api),
    path("donation_list_api/", views.donation_list_api),
    path("generate_unique_code_api/", views.generate_unique_code_api),
    path("search_serial_api/", views.search_serial_api),
    path("update_serial_api/", views.update_serial_api),
    path("serial_list_api/", views.serial_list_api),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




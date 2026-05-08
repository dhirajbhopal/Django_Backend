from django.urls import path
from core.views import ProfileView,Imageview,ProfileUpdate,mysingup,signuptask,forgotpassword,home
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from core import urls as core_urls
from django_user import urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup', mysingup.as_view(), name='signup'),
    path('signuptask', signuptask.as_view(), name='signuptask'),
    path('forgotpass', forgotpassword.as_view(), name='forgotpass'),
    path('resetpass', views.resetpass),
    path('imageupdate', views.Imageupdate),
    path('sendotp', views.sendotp),
    path('forgotsendotp', views.forgotsendotp),
    path('cheksignup', views.cheksignup),
    path('profile',ProfileView.as_view(), name='profile'),
    path('imageview',Imageview.as_view(), name='imageview'),
    path('profileupdate/<int:pk>', ProfileUpdate.as_view(),name='profileupdate'),
    path('addserialno', views.addserialno),
    path('searchserialno', views.searchserialno),
    path('editserialno', views.editserialno),
    path('gallery1', views.gallery1),
    path('gallery2', views.gallery2),
    path('gallery3', views.gallery3),
    path('donationdetail', views.donationdetail),
    path('donationlist', views.donationlist),
    path('logout', views.logoutUser, name="logout"),
    path('generate_unique_code', views.generate_unique_code, name="generate_unique_code"),
    path('searchserialnoall', views.searchserialnoall),
    path('publicsearch', views.publicsearch),
    path('publicsearchno', views.publicsearchno),
    path('', views.home.as_view(), name='home'),
    path('accounts/login/', views.home.as_view(), name='login'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
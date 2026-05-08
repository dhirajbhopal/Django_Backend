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


urlpatterns = [
    #path('__debug__/', include('debug_toolbar.urls')),
    path('pateladmin', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include(core_urls)),

    # Login and Logout
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='commons/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   
    # Main Page 
    #path('', TemplateView.as_view(template_name='base.html'), name='home'),

    # Change Password
    path('change-password',auth_views.PasswordChangeView.as_view(template_name='commons/change-password.html',success_url = '/'),
        name='change_password'),

    # Password Rest link Mail Genartaor

    path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='commons/password-reset/password_reset_form.html',
            email_template_name='commons/password-reset/password_reset_email.html',
            subject_template_name='commons/password-reset/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='commons/password-reset/password_reset_done.html'
        ), name='password_reset_done'),

    # link in email -> user clicks, sets new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='commons/password-reset/password_reset_confirm.html',
            success_url='/reset/done/'
        ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='commons/password-reset/password_reset_complete.html'
        ), name='password_reset_complete'),

        # Course view
    path('vision', TemplateView.as_view(template_name='site/vision.html'), name='vision'),

     # Contact
    path('contact', TemplateView.as_view(template_name='site/contactus.html'), name='contact'),

    # about view
    path('about', TemplateView.as_view(template_name='site/about.html'), name='about'),

    # donnation view
    path('donation', TemplateView.as_view(template_name='site/donation.html'), name='donation'),

    path('checkmail/', TemplateView.as_view(template_name='site/mail.html'), name='checkmail'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




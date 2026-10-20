import os
from pathlib import Path
import pymysql
import certifi
import ssl
import requests


# Allow PyMySQL to work as MySQLdb
pymysql.install_as_MySQLdb()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = '&#2uf8lms6l!ow)om51gr)70h4*#f$w=!)labd!t36(ua4z6hh'
DEBUG = False  # Turn off debug in production

APPEND_SLASH = True
SESSION_SAVE_EVERY_REQUEST = True

# Add your API subdomain here if you are using one (e.g., 'api.pjkss.com')
#ALLOWED_HOSTS = ['pjkss.com', 'www.pjkss.com', '127.0.0.1' , 'http://127.0.0.1:3000', 'pjkss.pythonanywhere.com']
ALLOWED_HOSTS = ['pjkss.pythonanywhere.com']

# CSRF and session cookies
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True


CORS_ALLOW_CREDENTIALS = True

# Allow your React origin (including www variant for production)
CORS_ALLOWED_ORIGINS = [
    "https://pjkss.com",
    "https://pjkss.pythonanywhere.com",
    "https://www.pjkss.com",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:3000"

]

CSRF_TRUSTED_ORIGINS = [
    "https://pjkss.com",
    "https://pjkss.pythonanywhere.com",
    "https://www.pjkss.com",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:3000"
]

SESSION_COOKIE_SAMESITE = "Lax"


# Application definition
# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'core',
    'django_user',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
   }

# MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must remain at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = 'django_user.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_user.wsgi.application'


# Database (MySQL) - FIXED HOST FOR CPANEL
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pjkssco1_pjkss_db',
        'USER': 'pjkssco1_pjkssdhiraj',
        'PASSWORD': 'patel@PJKSS#dehri$bihar%2026',
        'HOST': 'localhost',  # Connected locally inside cPanel
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}"""


# MySQL Database Configuration for pythonanywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pjkss$pjkss_db',
        'USER': 'pjkss',
        'PASSWORD': 'patel@PJKSS#dehri$bihar%2026',
        'HOST': 'pjkss.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
#new----------------------

# Page to go after successfull login
LOGIN_REDIRECT_URL = 'admin'

AUTH_USER_MODEL = "core.User"

# Email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pjkssinfo@gmail.com'
EMAIL_HOST_PASSWORD = 'bwqpbkcdutyqheoi'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
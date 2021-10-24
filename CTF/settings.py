"""
Django settings for CTF project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(os.path.join(BASE_DIR, '.env'))

if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_S3_REGION_NAME=os.environ['AWS_S3_REGION_NAME']
    AWS_STORAGE_BUCKET_NAME=os.environ['AWS_STORAGE_BUCKET_NAME']
    
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ['DEBUG']=='True')

ALLOWED_HOSTS = ['127.0.0.1', 'ctb-env.eba-2prnxpqz.ap-south-1.elasticbeanstalk.com', 'ctb.version21.in', 'ctb.vmothra.fun', '13.232.146.135']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_modal_forms',
    'accounts',
    'home',
    'challenges',
    'teams',
    'stats',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'CTF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'CTF.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
            #     "OPTION": {
            #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            # }
        }
    }
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
AWS_QUERYSTRING_AUTH = False
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [BASE_DIR/'static']

### Django storages - use this for production
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'challenges/uploads/')

### Django storages - use in production
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/challenges/'

# email configuration
# EMAIL_BACKEND='django_smtp_ssl.SSLEmailBackend'
# EMAIL_HOST='email-smtp.ap-south-1.amazonaws.com'
# EMAIL_PORT=465
# EMAIL_USE_SSL=True
# EMAIL_HOST_USER=os.environ['AWS_SES_SMTP_USER']
# EMAIL_HOST_PASSWORD=os.environ['AWS_SES_PASSWORD']
# DEFAULT_FROM_EMAIL=os.environ['AWS_SES_SENDER_EMAIL_ID']

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'ctb_send_mails'
EMAIL_HOST_PASSWORD  = os.environ["SENDGRID_API_KEY"]
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
DEFAULT_FROM_EMAIL=os.environ['DEFAULT_FROM_EMAIL']
SENDGRID_SANDBOX_MODE_IN_DEBUG = True
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Activate Django-Heroku.
# django_heroku.settings(locals())
"""
Django settings for airpapi project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from os import path
from django.utils.translation import ugettext_lazy as _
from urllib.parse import urljoin

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
MICROSERVICE_NAME="airpapi_web"
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DB_DIR = 'C:/Users/Antonio/Documents/bi/mydb.cnf'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Madrid'
# TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

LANGUAGES = (
    ('en', _('English'))
    ('es', _('Spanish'))
)

prefix_default_language = False  # Eliminar el prefijo del idioma by default

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# ================================ Congiruracion de docker ================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&+jc0^3qyuw(ep_j#f%sv%*f-+++ic+@pv)g+010z)jrnqmlq!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = (int(os.getenv('DEBUG', '0')) == 1)

# ALLOWED_HOSTS = []

if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # se pueden añadir otras ip

DEFAULT_PGSQL_HOST = os.getenv('POSTGRES_HOST','bzpro8nmnav7lcx1wfof-postgresql.services.clever-cloud.com')
DEFAULT_PGSQL_PORT = os.getenv('POSTGRES_PORT','5432')
DEFAULT_PGSQL_USER = os.getenv('POSTGRES_USER','uphbbfafkvwo5cfrwb4r')
DEFAULT_PGSQL_PASSWORD = os.getenv('POSTGRES_PASSWORD','vo5QlKsKgQB0JeuLcDf3')
DEFAULT_PGSQL_NAME = os.getenv('POSTGRES_DB','bzpro8nmnav7lcx1wfof')
#DEFAULT_PGSQL_SCHEMA = os.getenv('POSTGRES_SCHEMA','??')

# ================================ Configuracion de IU Swagger ================================

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': None
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'info.daliasoft@gmail.com'
# EMAIL_HOST_PASSWORD = 'pass'
# EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_swagger'
    'rest_framework.authtoken',
    'mama_cas',
    'django_cas_ng',
    'colorful',
    #'djoser',
    'api' # Added API
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FileUploadParser'
    ],
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination'
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'airpapi.urls'
#ROOT_URLCONF = '{}.urls'.format(MICROSERVICE_NAME)

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
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'airpapi.wsgi.application'
# WSGI_APPLICATION = '{}.wsgi.application'.format(MICROSERVICE_NAME)


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'OPTIONS': {
#            'read_default_file': DB_DIR,
#        },
#    }
#}

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        #'OPTIONS': {
        #        'options': '-c search_path={}'.format(DEFAULT_DB_SCHEMA)
        #    },
        'HOST': DEFAULT_PGSQL_HOST,
        'PORT': DEFAULT_PGSQL_PORT,
        'USER': DEFAULT_PGSQL_USER,
        'PASSWORD': DEFAULT_PGSQL_PASSWORD,
        'NAME': DEFAULT_PGSQL_NAME,
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# =========================== Configuracion CAS ===========================

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

LOGIN_URL = 'cas_ng_login'
LOGOUT_URL = 'cas_ng_logout'

CAS_ROOT_PROXIED_AS=os.getenv('MICROSERVICE_WEB_URL', 'http://127.0.0.1:8100').strip("/") # no poner barra / al final
CAS_SERVER_URL=urljoin(os.getenv('MICROSERVICE_WEB_URL', 'http://127.0.0.1:8100/'),'cas/')
CAS_VERSION = '3'
CAS_APPLY_ATTRIBUTES_TO_USER = True
CAS_LOGOUT_COMPLETELY = True


# =========================== MAMA CAS ===========================

MICROSERVICE_WEB_URL=os.getenv('MICROSERVICE_WEB_URL', 'http://127.0.0.1:8100/')
MICROSERVICE_CORE_URL=os.getenv('MICROSERVICE_CORE_URL', 'http://127.0.0.1:8101/')
MICROSERVICE_ML_URL=os.getenv('MICROSERVICE_ML_URL', 'http://127.0.0.1:8102/')
MICROSERVICE_RPA_URL=os.getenv('MICROSERVICE_RPA_URL', 'http://127.0.0.1:8103/')

SESSION_COOKIE_NAME = 'sessionid_server_cas'
MAMA_CAS_FOLLOW_LOGOUT_URL=True
MAMA_CAS_ENABLE_SINGLE_SIGN_OUT = True

MAMA_CAS_SERVICES = [
    {
        'SERVICE': MICROSERVICE_WEB_URL,
        'LOGOUT_ALLOW': True,
        'LOGOUT_URL': urljoin(MICROSERVICE_WEB_URL,'cas/accounts/callback/'),'CALLBACKS': [
            'mama_cas.callbacks.user_model_attributes',
        ],
    },
    {
        'SERVICE': MICROSERVICE_CORE_URL,
        'LOGOUT_ALLOW': True,
        'CALLBACKS': [
            'mama_cas.callbacks.user_model_attributes',
        ],
        'LOGOUT_URL': urljoin(MICROSERVICE_CORE_URL,'accounts/callback/'),
    },
    {
        'SERVICE': MICROSERVICE_RPA_URL,
        'LOGOUT_ALLOW': True,
        'CALLBACKS': [
            'mama_cas.callbacks.user_model_attributes',
        ],
        'LOGOUT_URL': urljoin(MICROSERVICE_ML_URL,'accounts/callback/'),
    }
]


# =========================== Date format ===========================

DATE_INPUT_FORMATS = (  # Formatos de fecha en campos de entrada aceptados
    '%d/%m/%Y', '%d/%m/%y',  # '25/10/2006', '25/10/06'
    '%d-%m-%Y', '%d-%m-%y',  # '25-10-2006', '25-10-06'
    '%d.%m.%Y', '%d.%m.%y',  # '25.10.2006', '25.10.06'
    '%d %b %Y',  # '25 Oct 2006',
    '%d %B %Y',  # '25 October 2006',
)
DATETIME_INPUT_FORMATS = {
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%Y@%H:%M:%S',  # '10/25/2006@14:30:59'
    '%m/%d/%y',  # '10/25/06'
}

# Date format always -> USE_L10N=False
SHORT_DATE_FORMAT = '%d-%m-y'
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
SHORT_DATETIME_FORMAT = '%d/%m/%y %H:%M:%S'

FIXTURE_DIRS= (path.join(PROJECT_ROOT, 'fixtures'), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = path.join(PROJECT_ROOT, 'collected_static')
LOGOUT_REDIRECT_URL="home"
import os
import configparser
from pathlib import Path


# Getting data from the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#  SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = fr'{config['settings_django']['SECRET_KEY']}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['settings_django']['DEBUG'] == 'True'

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.main',             # Main apps
    'apps.blog',             # Apps with blog
    'apps.newsletters',      # Apps with newsletters
    'apps.users',            # Apps with users
    'apps.clients',          # Apps with clients
    'apps.messages_',        # Apps with messages

    'django_apscheduler',  # Django apsheduler

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{config['database']['engine']}',
        'NAME': config['database']['dbname'],
        'USER': config['database']['user'],
        'PASSWORD': config['database']['password'],
        'HOST': config['database']['host'],
        'PORT': config['database']['port'],
    }
}


# Password validation
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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps', 'main', 'static'),
]


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Users
AUTH_USER_MODEL = 'users.Users'


# Login / Logout / Registry
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Data email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = config['data_email_yandex']['email_host_user']
EMAIL_HOST_PASSWORD = config['data_email_yandex']['email_host_password']

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

# Caches
CACHE_ENABLED = config['settings_django']['CACHE_ENABLED'] == 'True'
if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": config['settings_django']['LOCATION'],
        }
    }
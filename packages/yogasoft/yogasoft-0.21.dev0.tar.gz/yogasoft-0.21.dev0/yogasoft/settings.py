from __future__ import unicode_literals, absolute_import
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['yogasoft.codernetwork.ga',
                 'localhost',
                 'dev.yogasoft.codernetwork.ga']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'bootstrap3',
    'social_django',  # Lib for social networks auth
    'app.templatetags',
    'storages',
    's3direct',
    'django_cron',  # 10.07.2017 added to cron jobs
    'django_twilio',  # 16.07.2017 added for sms logger and send sms
    'channels',  # 24.07.2017 added to update comments of blog post
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # added 14.07.17 for cache
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware', # added for static files heroku
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # added 14.07.17 for cache

    # taras added 28.02.2017 to facebook login
    #'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'yogasoft.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'app/adm/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # For social auth
                'social_django.context_processors.login_redirect',  # For social auth
                'django.template.context_processors.i18n', # getting language code
            ],
        },
    },
]

WSGI_APPLICATION = 'yogasoft.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTHENTICATION_BACKENDS = (  # For social auth
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

CRON_CLASSES = ['app.cron.JustWriteTimeJob']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',
                                       default='SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',
                                          default='SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range'
}
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY',
                                  default='SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET',
                                     default='SOCIAL_AUTH_FACEBOOK_SECRET')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N, USE_L10N, USE_TZ = True, True, True

LANGUAGES = (
    ('uk', 'Ukrainian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# E-Mail settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='EMAIL_HOST_USER')

# twilio for sms
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = config('TWILIO_NUMBER', default='TWILIO_NUMBER')


SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'  # Redirect page after successful login
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


S3DIRECT_REGION = 'eu-west-1'
S3DIRECT_DESTINATIONS = {
    'example_destination': {
        # REQUIRED
        'key': '/',
        # OPTIONAL
        'auth': lambda u: u.is_staff, # Default allow anybody to upload
        'allowed': ['image/jpeg', 'image/png', 'video/mp4'],  # Default allow all mime types
        'bucket': 'yogasoftbucket0', # Default is 'AWS_STORAGE_BUCKET_NAME'
        'acl': 'private', # Defaults to 'public-read'
        'cache_control': 'max-age=2592000', # Default no cache-control
        'content_disposition': 'attachment',  # Default no content disposition
        'content_length_range': (5000, 20000000), # Default allow any size
        'server_side_encryption': 'AES256', # Default no encryption
    }
}

# for amazon web services
AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET_NAME', default='AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
#STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'static'),
)
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = '/yogasoft/static'
# used for url in producion prefix
STATIC_URL = '/static/'


if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL[1:])
else:
    #MEDIA_ROOT = '/yogasoft/media'
    #MEDIA_URL = '/media/'
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME', default='DATABASE_NAME'),
            'USER': config('DATABASE_USER', default='DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD', default='DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST', default='DATABASE_HOST'),
            'PORT': config('DATABASE_PORT', default='DATABASE_PORT'),
        }
    }
CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(config('REDIS_HOST', default='REDIS_HOST'),
                           int(config('REDIS_PORT', default=6379)))],
            },
            "TEST_CONFIG": {  # for testing channels added 01.08.2017
                "hosts": [("localhost", 6379)],
            },
            "ROUTING": "app.routing.channel_routing",
        },
    }


CELERY_BROKER_URL = config('REDIS_URL', default='REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# 11.07.2017  added caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 10,
    },
}

# 16.07.2017 added logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
            },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
            },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/', 'file.log'),
            'formatter': 'verbose',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
            },
        'sms_handler': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logs.logs.SmsHangler',
            'formatter': 'simple'
        }
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
            },
        'django.request': {
            'handlers': ['file', 'mail_admins', 'sms_handler'],
            'level': 'ERROR',
            'propagate': False,
            },
    }
}

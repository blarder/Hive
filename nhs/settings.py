"""
Django settings for nhs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vg4qfmtdt!f7lf*ov+55jzti2#qx7k4ew^-gxuo$fa0lzf7e17'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# PUSH NOTIFICATION SETTINGS

PUSH_NOTIFICATIONS_SETTINGS = {
    "APNS_CERTIFICATE": os.path.join(BASE_DIR, 'devices/apns_ck.pem'),
    "GCM_API_KEY": "AIzaSyA5id5lB7ilLA4qpt6OMRclLdxRSSIMpsc"
}

# FACEBOOK LOGIN SETTINGS

SOCIAL_AUTH_FACEBOOK_KEY = "648245191952694"
SOCIAL_AUTH_FACEBOOK_SECRET = "a16f5679303aff0df03338bf2a52f145"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


# Application definition

INSTALLED_APPS = (
    'sslserver',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'post_office',
    'cron_jobs',
    'users',
    'events',
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'devices',
    'djcelery'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True


ROOT_URLCONF = 'nhs.urls'

WSGI_APPLICATION = 'nhs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES_SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES_POSTGRESQL = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "nhs",
        "USER": "nhs",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "",
    }
}

### When syncing database, 'export DYLD_LIBRARY_PATH=/Library/PostgreSQL/9.3/lib' may be necessary on local machine
DATABASES = DATABASES_SQLITE3

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SESSION_COOKIE_SECURE = True
os.environ['HTTPS'] = 'on'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'testappblarder@gmail.com'
EMAIL_HOST_PASSWORD = 'testappblarder280'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

TEMPLATE_DIRS = (
    BASE_DIR + '/nhs/www',
)

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR + '/nhs/www',
)

# CELERY SETTINGS

BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

GRAPPELLI_INDEX_DASHBOARD = 'nhs.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'NHS Bank Admin'

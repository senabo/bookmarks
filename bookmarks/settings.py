import os
from django.urls import reverse_lazy
from . import secret

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = secret.SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = [
    'mysite.com',
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'images.apps.ImagesConfig',
    'actions.apps.ActionsConfig',

    # 'sorl.thumbnail',

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

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bookmarks.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = secret.EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    # 'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

# SOCIAL_AUTH_FACEBOOK_KEY = secret.SOCIAL_AUTH_FACEBOOK_KEY # Facebook App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = secret.SOCIAL_AUTH_FACEBOOK_SECRET # Facebook App Secret
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secret.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY  # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secret.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET  # Google Consumer Secret

LOGIN_REDIRECT_URL = 'dashboard'
# LOGIN_URL = 'login'
# LOGOUT_URL = 'logout'

# THUMBNAIL_BACKEND = 'thumbnails.models.SEOThumbnailBackend'

ADMINS = (
    ('Nazar', 'senabo33@gmail.com')
)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-hd0)4wslf8&=c*u(5j-9lcb1*%bzqvhoj8z*p66x50e3qv*f)i')
SHOW_SWAGGER = int(os.getenv('DJANGO_SHOW_SWAGGER', 0))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv('DEBUG', 1))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # packages
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'modeltranslation',
    'tinymce',

    # local apps
    'authentication',
    'base',
    'services'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'authentication.middlewares.UserAuthMiddleware',
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

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'x-api-key',
    'content-type',
    'Authorization'
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'default'),
        'USER': os.getenv('DB_USER', 'default'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'default'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.custom_JWT.CustomJWTAuthentication',
    )
}

JWT_USE = True
ACCESS_TOKEN_LIFETIME = timedelta(days=int(os.getenv('ACCESS_TOKEN_LIFETIME_DAYS', 1)))
REFRESH_TOKEN_LIFETIME = timedelta(days=int(os.getenv('REFRESH_TOKEN_LIFETIME_DAYS', 2)))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'jwt': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'SWAGGER_UI_REQUEST_HEADERS': [
        {
            'name': 'Authorization',
            'description': 'JWT Token',
            'value': 'Bearer <your_jwt_token_here>'
        },
    ],
    'LOGIN_URL': 'api/v1/auth/login',
    "DEFAULT_MODEL_RENDERING": "example"
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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

get_text = lambda x: x
LANGUAGES = {
    'uz': get_text('Uzbek'),
    'ru': get_text('Russian'),
    'en': get_text('English'),
}

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'width': '100%',
    'plugins': 'advlist autolink lists link image charmap preview anchor '
               'searchreplace visualblocks code fullscreen insertdatetime media table paste help',
    'toolbar': 'undo redo | styleselect | bold italic | link image media | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
    'image_advtab': True,  # Enables advanced image options
    'file_picker_callback': 'function(callback, value, meta) { \
        if (meta.filetype === "image") { \
            var input = document.createElement("input"); \
            input.setAttribute("type", "file"); \
            input.setAttribute("accept", "image/*"); \
            input.onchange = function() { \
                var file = this.files[0]; \
                var reader = new FileReader(); \
                reader.onload = function() { \
                    callback(reader.result, { alt: file.name }); \
                }; \
                reader.readAsDataURL(file); \
            }; \
            input.click(); \
        } \
    }',
    'entity_encoding': 'raw',  # Prevents encoding of special characters
    'valid_elements': '*[*]',  # Allows all elements and attributes (optional)
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
GOOGLE_ACCESS_JSON_NAME = os.getenv('GOOGLE_ACCESS_JSON_NAME')

SMS_BASE_URL = os.getenv('SMS_BASE_URL', 'https://example.com/')
SMS_USERNAME = os.getenv('SMS_USERNAME', '')
SMS_PASSWORD = os.getenv('SMS_PASSWORD', '')

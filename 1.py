import os

import environ

from pathlib import Path                                                                                            

# os.getenv() не вызывает исключение, но возвращает None
# os.environ.get() аналогично возвращает None
# os.environ[] вызывает исключение, если переменная окружения не существует
env = environ.Env(
    # set casting, default value
    DEBUG=(bool),
    SECRET_KEY=(str),

    DB_HOST=(str),
    DB_PORT=(str),
    POSTGRES_DB=(str),
    POSTGRES_USER=(str),
    POSTGRES_PASSWORD=(str),
    PGDATA=(str),

    PGADMIN_DEFAULT_EMAIL=(str),
    PGADMIN_DEFAULT_PASSWORD=(str),

    EMAIL_HOST=(str),
    EMAIL_PORT=(int),
    EMAIL_HOST_USER=(str),
    EMAIL_HOST_PASSWORD=(str),

    STRIPE_PUBLIC_KEY=(str),
    STRIPE_SECRET_KEY=(str),
    STRIPE_WEBHOOK_SECRET=(str),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = str(os.environ.get("SECRET_KEY"))
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = int(os.environ.get("DEBUG", default=0))
DEBUG = env('DEBUG')

# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS")
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
ALLOWED_HOSTS = ["*"]

DOMAIN_NAME = 'http://127.0.0.1:8000'  # 7.11, в 10.5 для оплаты

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # 8.4 и в админке добавилась таблица сайты
    'django.contrib.humanize',  # 10.4 улучшает показ цифр

    'allauth',  # 8.4
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',  # 8.4 для авторизации ч/з github
    'debug_toolbar',  # 9.7
    'django_extensions',  # 11.3 для shell-plus

    'rest_framework',  # 12.3
    'rest_framework.authtoken',  # 12.7

    'products',
    'users',
    'api',
    'orders',
    # 'django.contrib.postgres',  # это модуль Django, который предоставляет интеграцию с базой данных PostgreSQL
]                                                                                         

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # 9.7
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',  # если запускается удалить
]

ROOT_URLCONF = 'store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # 8.4 проверяем что есть, нужен для авторизации ч/з соцсети
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.context_processors.baskets',  # 7.13 контекстный процессор - выносим сюда то что часто используем
            ],
        },
    },
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'store_db_production',
        'USER': 'store_username_production',
        'PASSWORD': 'store_password_production',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = (
        BASE_DIR / 'static',
    )  # (для локальной разработки) по каким путям ходит collectstatic чтобы собрать их в STATIC_ROOT
    #  STATICFILES_DIRS и STATIC_ROOT не могут быть одновременно
else:  # 11.9 (для деплоя) по каким путям ходит NGINX чтобы собрать их в STATIC_ROOT
    # STATIC_ROOT = BASE_DIR / 'static'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 3.8 2:00 добавляем пути для медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Users
AUTH_USER_MODEL = 'users.User'  # 4.6
LOGIN_URL = '/users/login/'  # 5.5
LOGIN_REDIRECT_URL = '/'  # 7.7
LOGOUT_REDIRECT_URL = '/'  # 7.7


# Sending emails

if DEBUG:
    # для работы в консоли:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # для работы с почтой:
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False


# OAuth регистрация ч/з соцсети

AUTHENTICATION_BACKENDS = [  # 8.4
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1  # id сайта, если удалил и создал новый в админке тут id = 2

SITE_ID = 1  # id сайта, если удалил и создал новый в админке тут id = 2

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            # 'repo',  не нужны
            # 'read:org',  не нужны
        ],
    }
}


# Django REST framework  12.5

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3,
    # 'DEFAULT_AUTHENTICATION_CLASSES': [  базовые настройки, ставим свои ниже c TokenAuthentication
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [  # 12.7
         'rest_framework.authentication.TokenAuthentication'
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [  # 12.7 можно здесь, но сдлали во api/views.py через permission_classes
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

# Caches for Redis

#CACHES = {}

# CELERY

# CELERY_BROKER_URL = 'redis://127.0.0.1:6379' если не в докере
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379' если не в докере
# вариант записи:
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = '6379'
# CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
# CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_URL = 'redis://redis:6379/0'  # указываем django какой url будет у celery брокера(redis)
# redis:// - протокол по которому надо подключиться, 
# redis: - hostname который прописан в docker-compose, 6379 порт
# в конце можно добавить /0, /1... с какой бд (их несколько) в redis будем работать
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# STRIPE

STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")

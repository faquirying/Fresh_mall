"""
Django settings for FreshMall project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!rj!3zx70&@4&!2i2&nqv=b4#b=c+4v84urv7#g9)qoe(p^srq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Store',
    'Buyer',
    'djcelery',
    'ckeditor',
    'rest_framework',
    'ckeditor_uploader'
]

MIDDLEWARE = [
    # 一层层安检
    # 'django.middleware.cache.UpdateCacheMiddleware',  # 全栈粒度缓存配置首部
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'FreshMall.middleware.MiddlewareTest',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # 全栈粒度缓存配置尾部
]

ROOT_URLCONF = 'FreshMall.urls'

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

WSGI_APPLICATION = 'FreshMall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 为True 默认使用utc 0时区


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_ROOT = os.path.join(BASE_DIR, "static")  # 当前项目的静态文件根目录

CKEDITOR_UPLOAD_PATH = 'static/upload'  # 基于ckeditor的上传地址
CKEDITOR_IMAGE_BACKEND = 'pillow'  # ckeditor上传图片使用的模块

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],  # 权限
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,  # 分页
    'DEFAULT_RENDERER_CLASSES': (
        'utils.rendererresponse.Customrenderer',
    ),  # 自定义数据处理接口
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # django-filter 自带的查询过滤器
    )
}

# 配置邮件服务器
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # 发送邮件采用smtp服务

EMAIL_USE_TLS = False  # 使用tls方式

EMAIL_HOST = "smtp.qq.com"
EMAIL_POST = 456
EMAIL_HOST_USER = "215558997@qq.com"
EMAIL_HOST_PASSWORD = "xxxxx"
DEFAULT_FROM_EMAIL = "215558997@qq.com"


# celery配置
import djcelery  # 导入django-celery
djcelery.setup_loader()  # 进行模块加载
BROKER_URL = 'redis://127.0.0.1:6379/1' # 任务容器地址，redis数据库地址
CELERY_IMPORTS = ('CeleryTask.tasks')  # 具体的任务文件
CELERY_TIMEZONE = 'Asia/Shanghai'  # celery 时区
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # celery 处理器


# celery的定时器
from celery.schedules import crontab
from celery.schedules import timedelta

CELERYBEAT_SCHEDULE = {    # 定时器策略
    # 定时任务一：每隔30s运行一次
    u'测试定时器1': {
        "task": "CeleryTask.tasks.taskExample",
        # "schedule": crontab(minute='*/2'),  # or 'schedule': timedelta(seconds=3)
        "schedule": timedelta(seconds=3),
        "args": (),
    },
    u'来自小王的逼逼叨': {
        "task": "CeleryTask.tasks.DingTalk",
        "schedule": timedelta(seconds=3),
        "args": (),
    },
}


# cache需要有自己的配置，配置的结构，不需要手写，用global_settings中的cache配置
# D:\Anaconda3\envs\DjangoPath\Lib\site-packages\django\conf\global_settings
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', # 默认使用本地缓存
#     }
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',  # 申明使用memcache进行缓存
#         'LOCATION': [
#             '127.0.0.1:11211'
#         ]  # memcache 地址
#     }
# }

# Redis数据库缓存设置
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',  # 声明rediscache进行缓存
#         'LOCATION': [
#             'redis://127.0.0.1:6379/1'
#         ],  # memcache地址
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient'
#         }
#     }
# }

# 数据库缓存
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',  # 默认使用数据库缓存
#         'LOCATION': 'cache_table'  # 存放缓存的表
#     }
# }
# 全栈粒度缓存配置
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
# CACHE_MIDDLEWARE_SECONDS = 600
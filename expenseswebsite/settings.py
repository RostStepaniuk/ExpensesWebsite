"""
Django settings for expenseswebsite project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from django.contrib import messages

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [] #список разрешенние хостов 
#которые имеют право отправлять запросы на ваш Django-сервер
ALLOWED_HOSTS = ['*'] # all hosts
# ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # только локально


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',
    'userpreferences',
    'authentication',
    'userincome',
    'user_account'
]

#Middleware - это слой обработки 
# запросов и ответов между сервером и вашим Django-приложением.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#parametr определяет модуль, содержащий корневой URL-конфигурацию для вашего Django-проекта
ROOT_URLCONF = 'expenseswebsite.urls'

#настройки шаблонов для вашего Django-проекта
TEMPLATES = [
    {
        #определяет, какой шаблонный движок Django
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        #список директорий, где Django будет искать ваши собственные шаблоны
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        #Этот параметр указывает, что Django также должен искать шаблоны в директориях приложений
        'APP_DIRS': True,
        #настраивает контекстные процессоры для работы с шаблонами в Django
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

#место(приложение), где находится wsgi.py файл
# WSGI получает ЧТТП запрос от клиента , обрабативает и возвращает обратно клиенту
WSGI_APPLICATION = 'expenseswebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD':os.environ.get('DB_PASSWORD'),
        'HOST':os.environ.get('DB_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
#различние атрибути проверки пароля пользователя
#эти проверки активируются при использовании методов, таких как create_user() или set_password()
# при создании или обновлении учетных записей пользователей.
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
#временную зону, которая будет использоваться по умолчанию для вашего проекта
TIME_ZONE = 'UTC'
#настройка включает поддержку международных переводов (internationalization, i18n)
USE_I18N = True
#Эта настройка включает поддержку часовых поясов (timezone) в Django.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'expenseswebsite/static')]
#при развертывании приложения на сервере и выполнении команды collectstatic, 
# Django скопирует все статические файлы из директории expenseswebsite/static 
# в указанную директорию STATIC_ROOT,
STATIC_ROOT=os.path.join(BASE_DIR,'static')



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
# позволяет явно указать тип поля первичного ключа, чтобы избежать 
#   неоднозначности и предоставить большую гибкость при работе с базой данных.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#это словарь, который позволяет настраивать классы CSS для сообщений, 
#  которые выводятся пользователю при использовании механизма сообщений Django.
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


# email stuff
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')




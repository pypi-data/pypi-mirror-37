import sys, os
from django.core.management import utils
# from termcolor import colored
# from colorama import Fore, init

__version__ = "0.0.5"

project_name = sys.argv[1]
#second_arguement = sys.argv[2]

def main():
    #init()
    if '-' in project_name:
        print( "ERROR: Choose different name without using hyphen '-'")
        print("FAILED to create a new project.")
    else:
        # if second_arguement == '.':
        #     print(Fore.YELLOW + "WARNING: The project won't create in a current directory, Sorry for the inconvinience")

        # elif second_arguement:
        #     print(Fore.RED + "ERROR: It doesn't take second positional arguement")

        
        print("Executing django-babel version %s." % __version__)
        print("Creating a project: %s" % project_name)
        print("HAPPY CODING. :) ")
        ROOT_FOLDER = os.mkdir(str(project_name))

        ROOT_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name)
        MAIN_APP_NAME = os.mkdir(os.path.join(ROOT_PATH, project_name))
        STATIC_FOLDER = os.mkdir(os.path.join(ROOT_PATH, 'static'))
        TEMPLATES = os.mkdir(os.path.join(ROOT_PATH, 'templates'))

        STATIC_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static')
        MAIN_APP_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\' + project_name)
        TEMPLATES_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\templates')
        SETTINGS_FOLDER = os.mkdir(os.path.join(MAIN_APP_PATH, 'settings'))
        MAIN_APP_SETTINGS_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\' + project_name + '\\settings')

        STATIC_COMMON_FILES = os.mkdir(os.path.join(STATIC_PATH, 'common'))
        STATIC_HOME_FILES = os.mkdir(os.path.join(STATIC_PATH, 'home'))
        STATIC_DIST_FILES = os.mkdir(os.path.join(STATIC_PATH, 'dist'))

        STATIC_COMMON_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\common')
        STATIC_DIST_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\dist')
        STATIC_HOME_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\home')

        secret_key = utils.get_random_secret_key()

        # TEMPLATE FILE
        html= open(os.path.join(TEMPLATES_PATH, 'index.html'), "w+")
        html.write(
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Django Babel Boilerplate</title>
    {% load staticfiles %}
    {% load svg %}
    <link rel="stylesheet" href="{% static 'dist/css/index.css' %}">
</head>
<body>
  <style>
        .heading {
            text-align: center;
            font-family: sans-serif;
            font-size: 20px;
        }

        .creator {
            font-size: 16px;
        }

   </style>
    <h1 class="heading">DJANGO BABEL BOILERPLATE</h1>
    <h1 class="creator"><a href="https://www.navaneethnagesh.com/">Creator - Navaneeth Nagesh</a></h1>
</body>
</html>
""")
        html.close()

        # MAIN_APP_FILES
        wsgi= open(os.path.join(MAIN_APP_PATH, 'wsgi.py'), "w+")
        wsgi.write(
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", """ '"' + project_name + """.settings.local")

application = get_wsgi_application()
""")
        wsgi.close()

        views= open(os.path.join(MAIN_APP_PATH, 'views.py'), "w+")
        views.write(
"""
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
""")

        urls= open(os.path.join(MAIN_APP_PATH, 'urls.py'), "w+")
        urls.write(
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
]
""")
        urls.close()

        init_file= open(os.path.join(MAIN_APP_PATH, '__init__.py'), "w+")
        init_file.close()

        
        # SETTINGS BASE FILES

        staging= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'staging.py'), "w+")
        staging.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static-v1.0.0/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = '' + STATIC_URL
""")
        staging.close()

        production= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'production.py'), "w+")
        production.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

STATIC_URL = '/static-v1.0.0/'
STATIC_ROOT = '' + STATIC_URL

MEDIA_URL = '/'
MEDIA_ROOT = '/'
""")
        production.close()

        local= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'local.py'), "w+")
        local.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
""")
        local.close()

        base= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'base.py'), "w+")
        base.write(
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = """ "'" + secret_key + "'" """

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'svg'
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

ROOT_URLCONF = """ "'" + project_name + """.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = '""" + project_name + """.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
""")
        base.close()

        os.mkdir(os.path.join(STATIC_PATH, 'svg'))

        os.mkdir(os.path.join(STATIC_COMMON_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_COMMON_PATH, 'scss'))
    
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'css'))
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'images'))

        os.mkdir(os.path.join(STATIC_HOME_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_HOME_PATH, 'scss'))



        # ROOT FILES CREATION

        babelrc= open(os.path.join(ROOT_PATH, '.babelrc'),"w+")
        babelrc.write(
"""
{
    "presets": [
        "es2015"
    ]
}
""")
        babelrc.close() 
        
        requirements= open(os.path.join(ROOT_PATH, 'requirements.txt'), "w+")
        requirements.write(
"""
Django==2.1.1
django-inline-svg==0.1.1
pytz==2018.5
""")

        requirements_server= open(os.path.join(ROOT_PATH, 'requirements-server.txt'), "w+")
        requirements_server.write(
"""
Django==2.1.1
gunicorn==19.9.0
mysqlclient==1.3.13
pkg-resources==0.0.0
pytz==2018.5
""")
        requirements_server.close()

        package= open(os.path.join(ROOT_PATH, 'package.json'), "w+")
        package.write(
"""
{
  "name": """ '"'+ project_name +'"' """,
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "babel": "babel --watch --presets es2015 static/home/js static/common/js -d static/dist/js",
    "scss": "cd static && sass --watch common/scss:dist/css home/scss:dist/css",
    "server": "python manage.py runserver 0.0.0.0:8000",
    "start": "concurrently \\"npm run scss\\" \\"npm run babel\\" \\"npm run server\\""
  },
  "repository": {
    "type": "git",
    "url": ""
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "babel-cli": "^6.26.0",
    "babel-preset-es2015": "^6.24.1",
    "concurrently": "^4.0.1",
    "sass": "^1.14.1"
  }
}
""")
        package.close()
        
        manage= open(os.path.join(ROOT_PATH, 'manage.py'), "w+")
        manage.write(
"""
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__": 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", """ '"' + project_name + """.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

""")
        manage.close()

        gitignore= open(os.path.join(ROOT_PATH, '.gitignore'), "w+")
        gitignore.write(
"""
*.sqlite3
*.pyc
**/migrations/
**/.sass-cache/
*.map
.idea/
.vscode/
information/
all_staticfiles/
*.zip
node_modules/
static/uploaded/
virtualenv/
""")
        gitignore.close() 


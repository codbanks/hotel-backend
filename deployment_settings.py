import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

DEBUG = False
SECRET_KEY = os.getenviron.get['SECRET_KEY']

MIDDLEWARE = [
   'corshearder.middleware',
   'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddelware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddle',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessagesMiddleware',
]

CORS ALLOWED ORIGINS = [
    'https://hotel-frontend-1-yf6r.onrender.com'
]

STORAGES = {
  'default':{
    'BACKEND' : 'django.core.files.storage.fileSystemStorage',

  },
  'Staticfiles': {
    'BACKEND' : 'whotenoise.storage.CompressedStaticFileStorage',

  },
}

DATABASES = {
  'default': dj_database_url.config(
    default = os.environ['DATABASE_URL'],
    conn_max_age=600
  )
}
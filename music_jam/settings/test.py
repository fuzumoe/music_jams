import os

from .common import *

DEBUG = True

SECRET_KEY = "fm4vx26^1_jx34iiii^j_6&kn*31kazepkj581yr(!6(33hj-s"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'rest_framework.authtoken',
    'drf_spectacular',
    'music_jam.jams',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
import os
import mongoengine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "(=7t3%ya6s)gmgf1%4b6rar6zuel$x0go4ysi#g7n-lyed_z@#"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'core',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'course_api.urls'

TEMPLATES = []
WSGI_APPLICATION = 'course_api.wsgi.application'

# Disable Django's default DB
DATABASES = {}

# MongoDB Connection
mongoengine.connect(
    db="course_db",
    host="localhost",
    port=27017
)

# File Upload Settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

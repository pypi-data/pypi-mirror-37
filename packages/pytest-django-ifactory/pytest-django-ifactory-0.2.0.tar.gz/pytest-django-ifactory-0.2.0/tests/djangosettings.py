"""Django settings for pytest-django-ifactory's unit tests."""

from __future__ import unicode_literals

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0ay!$_8q2x7fo1bza(@1ovtudbu&1x=!7tzqa#a$cc8x@4o0m3"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.gis",
    "testapp",
]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": "pytestdjangoifactory.sqlite3",
    }
}

SPATIALITE_LIBRARY_PATH = os.environ.get("SPATIALITE_LIBRARY_PATH")

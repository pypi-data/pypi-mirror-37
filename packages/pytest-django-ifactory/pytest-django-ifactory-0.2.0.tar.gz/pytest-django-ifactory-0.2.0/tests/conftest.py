"""Test configuration for pytest-django-ifactory."""

from __future__ import unicode_literals

import os

from django.conf import settings
import py
import pytest

pytest_plugins = ["pytester"]


def pytest_configure():
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.contrib.gis.db.backends.spatialite"}},
        SPATIALITE_LIBRARY_PATH=os.environ.get("SPATIALITE_LIBRARY_PATH"),
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.gis",
            "testapp",
        ],
        USE_TZ=True,
    )


@pytest.fixture
def django_testdir(testdir):
    cwd = py.path.local(__file__).dirpath()
    cwd.join("djangosettings.py").copy(testdir.tmpdir)
    cwd.join("testapp").copy(testdir.tmpdir.join("testapp"))
    return testdir

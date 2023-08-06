"""Unit tests for pytest-django-ifactory's top-level package."""

from __future__ import unicode_literals

import pytest_django_ifactory


def test_version():
    assert pytest_django_ifactory.__version__ is not None

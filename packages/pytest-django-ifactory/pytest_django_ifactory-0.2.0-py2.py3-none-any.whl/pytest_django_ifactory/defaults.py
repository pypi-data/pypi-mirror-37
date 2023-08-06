"""Default value generation for model fields."""

from __future__ import unicode_literals

import datetime
import itertools
import string

from django.contrib.gis.db import models
from django.utils import timezone

try:
    from django.contrib.postgres import fields as postgres
except ImportError:  # psycopg2 is probably not available
    postgres = None


_generators = {}


def register(field_class, generator=None):
    """Register a default value generator for a field class."""

    def decorator(generator):
        _generators[field_class] = generator

    if generator is None:
        return decorator
    decorator(generator)


def generate_default_value(field, unique=False):
    """Generate a default value for a model field."""

    def _default_generator(field, unique=False):
        if unique:
            raise ValueError("unique not supported")
        return None

    generator = _generators.get(type(field), _default_generator)
    return generator(field, unique=unique)


@register(models.BooleanField)
def boolean_field_default(field, unique=False):
    if unique or field.unique:
        raise ValueError("unique not supported")
    return True


def char_field_default(field, unique=False):
    length = min(4, field.max_length or 4)
    if unique or field.unique:
        it = itertools.permutations(string.ascii_letters, length)
        return lambda: "".join(next(it))
    return "" if field.blank else "abcd"[:length]


register(models.CharField, char_field_default)
register(models.FileField, char_field_default)
register(models.ImageField, char_field_default)
register(models.SlugField, char_field_default)
register(models.TextField, char_field_default)


@register(models.DateField)
def date_field_default(field, unique=False):
    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count(step=24 * 60 ** 2)
        return lambda: datetime.date.fromtimestamp(next(it))
    return datetime.date.fromtimestamp(0)


@register(models.DateTimeField)
def date_time_field_default(field, unique=False):
    def todatetime(timestamp):
        t = datetime.datetime.utcfromtimestamp(timestamp)
        return timezone.make_aware(t, timezone.utc)

    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count(step=60 ** 2)
        return lambda: todatetime(next(it))
    return todatetime(0)


@register(models.FloatField)
def float_field_default(field, unique=False):
    if unique or field.unique:
        it = itertools.count()
        return lambda: float(next(it))
    return 0.0


def integer_field_default(field, unique=False):
    if unique or field.unique:
        it = itertools.count()
        return lambda: next(it)
    return 0


register(models.BigIntegerField, integer_field_default)
register(models.DecimalField, integer_field_default)
register(models.IntegerField, integer_field_default)
register(models.PositiveIntegerField, integer_field_default)
register(models.PositiveSmallIntegerField, integer_field_default)
register(models.SmallIntegerField, integer_field_default)


@register(models.TimeField)
def time_field_default(field, unique=False):
    def totime(timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).time()

    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count()
        return lambda: totime(next(it))
    return totime(0)


def make_geometry_field_default(template):
    def _default(field, unique=False):
        if unique or field.unique:
            it = itertools.count(1)
            return lambda: template % next(it)
        return template % 1

    return _default


for field, template in [
    (models.GeometryField, "POINT (%d 0)"),
    (models.PointField, "POINT (%d 0)"),
    (models.LineStringField, "LINESTRING (%d 0, 0 1)"),
    (models.PolygonField, "POLYGON ((0 0, %d 1, 0 1, 0 0))"),
    (models.MultiPointField, "MULTIPOINT ((%d 0))"),
    (models.MultiLineStringField, "MULTILINESTRING ((%d 0, 0 1))"),
    (models.MultiPolygonField, "MULTIPOLYGON (((0 0, %d 1, 0 1, 0 0)))"),
    (models.GeometryCollectionField, "GEOMETRYCOLLECTION (POINT (%d 0))"),
]:
    register(field, make_geometry_field_default(template))


if postgres:

    @register(postgres.JSONField)
    def json_field_default(field, unique=False):
        if unique or field.unique:
            raise ValueError("unique not supported")
        return {}

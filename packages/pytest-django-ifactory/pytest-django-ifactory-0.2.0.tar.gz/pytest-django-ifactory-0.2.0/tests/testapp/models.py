"""Django database models for pytest-django-ifactory's unit tests."""

from __future__ import unicode_literals

from django.contrib.gis.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=64)
    blank = models.CharField(max_length=64, blank=True)


class ModelB(models.Model):
    name = models.CharField(max_length=64, unique=True)
    required_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    nullable_a1 = models.ForeignKey(
        ModelA, on_delete=models.CASCADE, null=True, related_name="+"
    )
    nullable_a2 = models.ForeignKey(
        ModelA, on_delete=models.CASCADE, null=True, related_name="+"
    )


class AllFieldsModel(models.Model):
    boolean = models.BooleanField()
    char = models.CharField(max_length=32)
    file = models.FileField()
    image = models.ImageField()
    slug = models.SlugField()
    text = models.TextField()
    date = models.DateField()
    datetime = models.DateTimeField()
    float = models.FloatField()
    biginteger = models.BigIntegerField()
    decimal = models.DecimalField(decimal_places=0, max_digits=9)
    integer = models.IntegerField()
    positiveinteger = models.PositiveIntegerField()
    positivesmallinteger = models.PositiveSmallIntegerField()
    smallinteger = models.SmallIntegerField()
    time = models.TimeField()
    geometry = models.GeometryField()
    point = models.PointField()
    linestring = models.LineStringField()
    polygon = models.PolygonField()
    multipoint = models.MultiPointField()
    multilinestring = models.MultiLineStringField()
    multipolygon = models.MultiPolygonField()
    geometrycollection = models.GeometryCollectionField()

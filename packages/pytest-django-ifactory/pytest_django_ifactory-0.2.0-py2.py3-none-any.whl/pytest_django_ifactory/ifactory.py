"""The Django model instance factory."""

from __future__ import unicode_literals

import collections

from django.apps import apps as django_apps
from django.db import models
import six


def generate_default_value(*args, **kwargs):
    # The defaults module's imports use the Django settings so we
    # delay this import as long as possible
    from .defaults import generate_default_value as _generate_default_value

    return _generate_default_value(*args, **kwargs)


class CreateRelatedInstance(object):

    """Flag for creating a related instance using the factory.

    Any *attrs* given to the constructor will be used when creating
    the related instance.

    """

    def __init__(self, **attrs):
        self.attrs = attrs


class LookupRelatedInstance(object):

    """Flag for looking up a related instance in the database.

    The *attrs* given to the constructor must uniquely identify the
    related instance in the database.

    """

    def __init__(self, **attrs):
        self.attrs = attrs


class Unique(object):

    """Flag for generating a unique value for a field."""


class ApplicationNamespaceDescriptor(object):

    """Descriptor for an application namespace on an instance factory.

    Each instance of this class dynamically generates a namespace
    class for the *models* its given.

    """

    def __init__(self, models):
        class ApplicationNamespace(object):
            def __init__(self, ifactory):
                self.ifactory = ifactory

        # We can probably use functools.partialmethod when dropping
        # support for Python 2.7.
        def make_create(model):
            def create(self, **attrs):
                return self.ifactory.create(model, attrs)

            create.__name__ = model._meta.model_name
            return create

        for model in models:
            setattr(ApplicationNamespace, model._meta.model_name, make_create(model))

        self.namespace_class = ApplicationNamespace

    def __get__(self, instance, owner):
        return self.namespace_class(instance)


class InstanceFactory(object):

    """A factory for Django model instances to use in unit tests."""

    Create = CreateRelatedInstance
    Lookup = LookupRelatedInstance
    Unique = Unique

    # Global defaults for all models in the format
    # {model_label_lower: {field_name: default_value, ...}, ...}.
    _defaults = {}

    @classmethod
    def register_all_models(cls):
        """Register all installed models for production at the factory."""
        if not django_apps.ready:
            raise RuntimeError(
                "InstanceFactory.register_models() must be called after Django has "
                "been initialized"
            )
        for app in django_apps.get_app_configs():
            models = list(app.get_models())
            for model in models:
                cls._set_initial_defaults(model)
            setattr(cls, app.label, ApplicationNamespaceDescriptor(models))

    @classmethod
    def _set_initial_defaults(cls, model):
        # Generate initial default values for the fields of a *model*.
        def needs_default(field):
            return (
                not field.null
                and not field.has_default()
                and not isinstance(field, models.AutoField)
                and not field.many_to_many
                and not field.one_to_many
            )

        def generate_default(field):
            if field.many_to_one or field.one_to_one:
                return InstanceFactory.Create
            else:
                return generate_default_value(field)

        cls._defaults[model._meta.label_lower] = {
            field.name: generate_default(field)
            for field in model._meta.get_fields()
            if needs_default(field)
        }

    @classmethod
    def configure_defaults(cls, model, attrs):
        """Configure the default values for the given *model*.

        *model* can be an actual model class or a model label. *attrs*
        should map field names to default values.

        """

        def isunique(value):
            return value is cls.Unique or isinstance(value, cls.Unique)

        if isinstance(model, six.string_types):
            model = django_apps.get_model(model)
        if not cls._defaults:  # make sure the factory is initialized
            cls.register_all_models()
        cls._defaults[model._meta.label_lower].update(
            {
                name: generate_default_value(model._meta.get_field(name), unique=True)
                if isunique(value)
                else value
                for name, value in attrs.items()
            }
        )

    def __init__(self):
        if not self._defaults:  # make sure the factory is initialized
            self.register_all_models()

    def create(self, model, attrs=()):
        """Create an instance of the given model.

        This is the generic and more low-level method to create model
        instances. It can be useful if the model is not known before
        runtime. Otherwise, use the ifactory.applabel.modelname()
        shortcuts for this method.

        """

        def get_default_value(field, value):
            if value is self.Create:
                value = self.create(field.related_model)
            elif isinstance(value, self.Create):
                value = self.create(field.related_model, value.attrs)
            elif value is self.Lookup:
                value = field.related_model.objects.first()
            elif isinstance(value, self.Lookup):
                value = field.related_model.objects.get(**value.attrs)
            elif isinstance(value, collections.Callable):
                value = value()
            return value

        defaults = dict(
            (k, get_default_value(model._meta.get_field(k), v))
            for k, v in self._defaults[model._meta.label_lower].items()
            if k not in attrs
        )
        defaults.update(attrs)
        instance = model(**defaults)
        instance.clean()
        instance.save()
        return instance

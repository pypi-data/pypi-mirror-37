"""Unit and regression tests for the instance factory class."""

from __future__ import unicode_literals

import copy

import pytest
import six
from testapp.models import ModelA, ModelB


@pytest.fixture(params=["ifactory", "transactional_ifactory"])
def ifactory(request):
    return request.getfixturevalue(request.param)


def test_all_fields(ifactory):
    instance = ifactory.testapp.allfieldsmodel()
    for field in instance._meta.get_fields():
        assert getattr(instance, field.name) is not None


def test_initialization(ifactory):
    assert hasattr(ifactory, "testapp")
    assert hasattr(ifactory.testapp, "modela")
    assert hasattr(ifactory.testapp, "modelb")
    assert isinstance(ifactory.testapp.modela().name, six.text_type)
    b = ifactory.testapp.modelb()
    assert isinstance(b.name, six.text_type)
    assert isinstance(b.required_a, ModelA)
    assert b.nullable_a1 is None
    assert b.nullable_a2 is None


def test_blank_default(ifactory):
    a = ifactory.testapp.modela()
    assert not a.blank


def test_create_with_attrs(ifactory):
    assert ifactory.testapp.modela(name="foo").name == "foo"


def test_dynamic_method_names(ifactory):
    assert ifactory.testapp.modela.__name__ == "modela"
    assert ifactory.testapp.modelb.__name__ == "modelb"


class TestConfigure:
    @pytest.fixture
    def cifactory(self, ifactory):
        original_defaults = copy.deepcopy(ifactory._defaults)
        yield ifactory
        type(ifactory)._defaults = original_defaults

    @pytest.mark.parametrize("model", ["testapp.modelb", ModelB])
    def test_primitive(self, cifactory, model):
        cifactory.configure_defaults(model, {"name": "foo"})
        b = cifactory.testapp.modelb()
        assert b.name == "foo"

    def test_callable(self, cifactory):
        cifactory.configure_defaults("testapp.modela", {"name": lambda: "foo"})
        assert cifactory.testapp.modela().name == "foo"

    @pytest.mark.parametrize("model", ["testapp.NoModel", "noapp.NoModel"])
    def test_invalid_model(self, cifactory, model):
        with pytest.raises(LookupError):
            cifactory.configure_defaults(model, {})

    def test_create(self, cifactory):
        cifactory.configure_defaults(
            "testapp.modelb", {"nullable_a1": cifactory.Create}
        )
        assert isinstance(cifactory.testapp.modelb().nullable_a1, ModelA)

    def test_create_with_attrs(self, cifactory):
        cifactory.configure_defaults(
            "testapp.modelb", {"nullable_a1": cifactory.Create(name="foo")}
        )
        assert cifactory.testapp.modelb().nullable_a1.name == "foo"

    def test_lookup(self, cifactory):
        ModelA.objects.create(name="foo")
        ModelA.objects.create(name="bar")
        cifactory.configure_defaults(
            "testapp.modelb", {"nullable_a1": cifactory.Lookup}
        )
        assert cifactory.testapp.modelb().nullable_a1.name == "foo"

    def test_lookup_with_attrs(self, cifactory):
        ModelA.objects.create(name="foo")
        cifactory.configure_defaults(
            "testapp.modelb", {"nullable_a1": cifactory.Lookup(name="foo")}
        )
        assert cifactory.testapp.modelb().nullable_a1.name == "foo"

    def test_unique(self, cifactory):
        cifactory.configure_defaults("testapp.modela", {"category": cifactory.Unique})
        instance1 = cifactory.testapp.modela()
        instance2 = cifactory.testapp.modela()
        assert instance1.category != instance2.category

    def test_plugin(self, cifactory):
        cifactory.configure_defaults("testapp.ModelA", {"name": "adam"})
        cifactory.configure_defaults(
            "testapp.ModelB", {"name": "bert", "nullable_a1": cifactory.Create}
        )

        a = cifactory.testapp.modela(name="alan")
        assert ModelA.objects.count() == 1
        assert a.name == "alan"
        b = cifactory.testapp.modelb(required_a=a)
        assert ModelB.objects.count() == 1
        assert ModelA.objects.count() == 2
        assert b.name == "bert"
        assert b.required_a is a
        assert isinstance(b.nullable_a1, ModelA)
        assert b.nullable_a1.name == "adam"
        assert b.nullable_a2 is None

[![pipeline status](https://gitlab.com/mjakob422/pytest-django-ifactory/badges/develop/pipeline.svg)](https://gitlab.com/mjakob422/pytest-django-ifactory/commits/develop)
[![coverage report](https://gitlab.com/mjakob422/pytest-django-ifactory/badges/develop/coverage.svg)](https://gitlab.com/mjakob422/pytest-django-ifactory/commits/develop)

# pytest-django-ifactory

A model instance factory for [pytest-django][].

[pytest-django]: https://pytest-django.readthedocs.io/

## Motivation

pytest-django-ifactory makes it easy to create model instances for
your test cases even if they contain a lot of non-nullable fields and
complex foreign key relationships. If you every felt like you spent
too much time coming up with dummy values for you models' fields just
to get an instance into the database to use in a test then
pytest-django-ifactory might be for you.

pytest's fixtures are great and perfect if you want to have a static
model instance available in the database for your tests. Problems
arise however when you want to vary one of its fields. To reuse your
fixture in that case you need to modify the field and save the
instance back to the database (assuming your test needs it in the
database, of course). This results in at least two lines of extra
setup code in you test case and an extra call to the database.

pytest-django-ifactory is simply an instance factory (hence
*ifactory*) function that automatically detects your Django models and
tries to come up with acceptable defaults for the fields you don't
care about. This includes generating unique values for fields marked
as unique and to create related instances for non-nullable foreign
keys.

## Usage

**Note that this library is very much in alpha and its API may change
in future versions.**

This plugin comes with two fixtures: `ifactory` and
`transactional_ifactory`.  Use them when you need to put model
instances in the database.  `ifactory` and `transactional_ifactory`
are identical except that the latter uses [pytest-django][]'s
`transactional_db` fixture instead of the `db` fixture.  See
pytest-django's and Django's documentation for when you would want to
use it.  Below is a contrived example to test a function that finds
duplicate names of your users:

```python
from itertools import groupby
from operator import methodcaller

from django.contrib.auth.models import User


def get_duplicate_names():
    all_users = User.objects.order_by("last_name", "first_name")
    users_by_name = groupby(all_users, methodcaller("get_full_name"))
    return [full_name for full_name, users in users_by_name if len(list(users)) > 1]


def test_get_duplicate_names(ifactory):
    ifactory.auth.user(first_name="Albert", last_name="Einstein")
    ifactory.auth.user(first_name="Albert", last_name="Einstein")
    ifactory.auth.user(first_name="Erwin", last_name="Schrodinger")
    ifactory.auth.user(first_name="Richard", last_name="Feynman")
    assert get_duplicate_names() == ["Albert Einstein"]
    assert User.objects.count() == 4
```

You find you models namespaced by the application name and the model
name on the `ifactory` instance. For instance, if you have created a
`Book` model in a `library` application (and put your library
application in INSTALLED_APPS), its factory function will be
`ifactory.library.book()`. This function accepts the same arguments as
your model constructor does and returns the created instance.

Notice in the example above that we create four new users without
specifying their unique usernames. The goal of this project is that
you should never have to specify the value of a field if you're not
interested in that value in your test. Conversely, you should never
rely on a value you haven't explicity set. This library gives no
guarantees that the value it chooses for a field will be the same the
next time the test is run. It just tries to make sure that the
instance can be saved to the database without any integrity errors.

While I would recommend against it, if you do want to know which
default value will be used, you can use the
`pytest_django_ifactory_configure` hook. A good place to put it is in
your *conftest.py*:

```python
def pytest_django_ifactory_configure(ifactory):
    ifactory.configure_defaults("auth.user", {
        "first_name": "Albert",
        "last_name": "Einstein",
    })
```

From now on, all users in your tests will be Albert Einstein unless
you say otherwise:

```python
def test_albert_by_default(ifactory):
    albert = ifactory.auth.user()
    assert albert.get_full_name() == "Albert Einstein"
    not_albert = ifactory.auth.user(first_name="Erwin", last_name="Schrodinger")
    assert not_albert.full_name() == "Erwin Schrodinger"
```

While the above example might not be the best idea as your test suit
grows the hook can be used to enforce constraints in your models that
this library is unaware of, e.g., validation errors raised by your
models that depend on the model's field values.

## Development

This project uses [black][] to auto-format the code, [flake8][] to
check it, [pytest][] to test it, and finally [check-manifest][] to
check the project's [MANIFEST.in](MANIFEST.in). To facilitate (and
remember) to actually run all these tools, [pre-commit][] is
used. Hence, the only hard development requirement is
*pre-commit*. Install it and run

```console
$ pre-commit install
```

once the first time you check out the repo and from now on all checks
except the unit tests will be run everytime a commit is made. The unit
tests are run manually with pytest

```console
$ pytest
```

Gitlab CI is configured to run the tests with Python 2.7 and 3.4-3.7
and all supported Django versions.

If you want to install all development requirements to run them
manually (and without using `pre-commit run --all-files`), use the
[requirements.txt](requirements.txt) file:

```console
$ pip install -r requirements.txt
```

[black]: https://github.com/ambv/black
[check-manifest]: https://github.com/mgedmin/check-manifest
[flake8]: https://gitlab.com/pycqa/flake8
[pre-commit]: https://github.com/pre-commit/pre-commit
[pytest]: http://pytest.org/

## License

Like [pytest-django][], pytest-django-ifactory is released under the
[BSD 3-clause](LICENSE) license.

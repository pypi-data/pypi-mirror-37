Podiant tours
=============

![Build](https://git.steadman.io/podiant/tours/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/tours/badges/master/coverage.svg)

A simple model to keep track of Bootstrap Tours delivered to new users

## Quickstart

Install Tours:

```sh
pip install podiant-tours
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'tours',
    ...
)

```
Add Tours' URL patterns:

```python
from tours import urls as tours_urls

urlpatterns = [
    ...
    url(r'^', include(tours_urls)),
    ...
]
```

## Running tests

Does the code actually work?

```
coverage run --source tours runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

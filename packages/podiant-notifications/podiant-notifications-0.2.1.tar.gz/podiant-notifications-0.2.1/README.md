Podiant notifications
=====================

![Build](https://git.steadman.io/podiant/notifications/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/notifications/badges/master/coverage.svg)

A set of models, views and templates for creating and managing user notifications

## Quickstart

Install Notifications:

```sh
pip install podiant-notifications
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'notifications',
    ...
)

```
Add Notifications' URL patterns:

```python
from notifications import urls as notifications_urls

urlpatterns = [
    ...
    url(r'^', include(notifications_urls)),
    ...
]
```

## Running tests

Does the code actually work?

```
coverage run --source notifications runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

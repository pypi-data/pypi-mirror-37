Podiant webhooks
================

![Build](https://git.steadman.io/podiant/webhooks/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/webhooks/badges/master/coverage.svg)

A super-simple, arbitrary webhook client

## Quickstart

Install Webhooks:

```sh
pip install podiant-webhooks
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'webhooks',
    ...
)
```

## Running tests

Does the code actually work?

```
coverage run --source webhooks runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

Podiant PubSub
==============

![Build](https://git.steadman.io/podiant/pubsub/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/pubsub/badges/master/coverage.svg)

A simpler, more flexible form of Django signals

## Quickstart

Install PubSub:

```sh
pip install podiant-pubsub
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'pubsub',
    ...
)
```

## Running tests

Does the code actually work?

```
coverage run --source pubsub runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

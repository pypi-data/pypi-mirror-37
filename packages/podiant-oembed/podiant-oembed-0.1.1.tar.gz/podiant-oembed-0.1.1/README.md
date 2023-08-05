Podiant oEmbed
==============

![Build](https://git.steadman.io/podiant/oembed/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/oembed/badges/master/coverage.svg)

A simple, flexible oEmbed provider and consumer

## Quickstart

Install oEmbed:

```sh
pip install podiant-oembed
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'oembed',
    ...
)
```

## Running tests

Does the code actually work?

```
coverage run --source oembed runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

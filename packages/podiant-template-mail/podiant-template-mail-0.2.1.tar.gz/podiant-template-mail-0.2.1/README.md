Podiant template mail
=====================

![Build](https://git.steadman.io/podiant/template-mail/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/template-mail/badges/master/coverage.svg)

A helper library for asynchronously sending HTML emails written in Markdown

## Quickstart

Install Template Mail:

```sh
pip install podiant-template-mail
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'template_mail',
    ...
)
```

Add Template Mail's URL patterns:

```python
from template_mail import urls as template_mail_urls

urlpatterns = [
    ...
    url(r'^', include(template_mail_urls)),
    ...
]
```


## Running tests

Does the code actually work?

```
coverage run --source template_mail runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)

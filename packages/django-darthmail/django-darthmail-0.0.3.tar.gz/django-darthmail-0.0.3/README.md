# django-darthmail

Module for using darthmail as an EMAIL\_BACKEND in Django.

# Settings

```python
EMAIL_BACKEND = 'django_darthmail.backends.DarthMailBackend'
EMAIL_DARTHMAIL_URL = 'https://some.darthmail.instance.url'
EMAIL_DARTHMAIL_TOKEN = 'someauthtoken'
EMAIL_DARTHMAIL_FALLBACK = 'django.core.mail.backends.smtp.EmailBackend'
```

# Making a new release

[bumpversion](https://github.com/peritus/bumpversion) is used to manage releases.

After reaching a releasable state, run `bumpversion <major|minor|patch>`, then `./setup.py publish`
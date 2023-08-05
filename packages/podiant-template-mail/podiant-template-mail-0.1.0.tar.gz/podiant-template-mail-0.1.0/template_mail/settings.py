from django.conf import settings as site_settings


__all__ = [
    'SITE_DOMAIN',
    'SITE_SSL'
]


SITE_DOMAIN = getattr(site_settings, 'SITE_DOMAIN', 'example.com')
SITE_SSL = getattr(site_settings, 'SITE_SSL', False)

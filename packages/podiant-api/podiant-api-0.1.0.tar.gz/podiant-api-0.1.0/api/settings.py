from django.conf import settings as site_settings


DEFAULT_AUTHORISERS = getattr(
    site_settings,
    'API_DEFAULT_AUTHORISERS',
    ['api.authorisation.GuestReadOnlyOrDjangoUserAuthoriser']
)

DEFAULT_RPP = getattr(
    site_settings,
    'API_DEFAULT_RPP',
    100
)

DEBUG = getattr(
    site_settings,
    'API_DEBUG',
    getattr(site_settings, 'DEBUG', False)
)

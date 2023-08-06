from django.conf import settings as site_settings
from django.template.defaultfilters import slugify
from .settings import URL_OVERRIDES


def get_type_name(obj):
    return slugify(obj._meta.verbose_name_plural)


def get_id_field(obj):
    m = '%s.%s' % (
        obj._meta.app_label,
        obj._meta.model_name
    )

    if m in URL_OVERRIDES:
        field, expr = URL_OVERRIDES[m]
        return field

    return 'pk'


def get_object_id(obj):
    m = '%s.%s' % (
        obj._meta.app_label,
        obj._meta.model_name
    )

    if m in URL_OVERRIDES:
        field, expr = URL_OVERRIDES[m]
        return str(expr(obj))

    return str(obj.pk)


def urlise_field_name(name):
    return name.replace('_', '-')


def unurlise_field_name(name):
    return name.replace('-', '_')


def get_authenticators():
    return getattr(
        site_settings,
        'API_DEFAULT_AUTHENTICATORS',
        ['api.authentication.DjangoSessionAuthenticator']
    )


def get_authorisers():
    return getattr(
        site_settings,
        'API_DEFAULT_AUTHORISERS',
        ['api.authorisation.GuestReadOnlyOrDjangoUserAuthoriser']
    )

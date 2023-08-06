from django.conf import settings as site_settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.template.defaultfilters import slugify
from logging import getLogger
from .settings import URL_OVERRIDES


def get_type_name(obj):
    return slugify(obj._meta.verbose_name_plural)


def get_object_url(obj):
    logger = getLogger('podiant.api')
    name = 'api:%s_%s_detail' % (
        obj._meta.app_label,
        obj._meta.model_name
    )

    m = '%s.%s' % (
        obj._meta.app_label,
        obj._meta.model_name
    )

    if m in URL_OVERRIDES:
        field, expr = URL_OVERRIDES[m]
        kwargs = {
            field: expr(obj)
        }
    else:
        kwargs = {
            'pk': obj.pk
        }

    try:
        return reverse(name, kwargs=kwargs)
    except NoReverseMatch:  # pragma: no cover
        logger.warning(
            (
                'No URL pattern found for %s.%s detail view ('
                'tried named URL pattern \'%s\')'
            ) % (
                obj._meta.app_label,
                obj._meta.model_name,
                name
            ),
            exc_info=True
        )


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


def get_relation_url(parent_model, parent_field, child_model, **kwargs):
    logger = getLogger('podiant.api')
    opts = parent_model._meta
    name = 'api:%s_%s_%s' % (
        opts.app_label,
        opts.model_name,
        parent_field
    )

    try:
        return reverse(name, kwargs=kwargs)
    except NoReverseMatch:  # pragma: no cover
        logger.warning(
            (
                'No API endpoint found to return '
                'relation between %s.%s and %s.%s (tried '
                'named URL pattern \'%s\')'
            ) % (
                opts.app_label,
                opts.model_name,
                child_model._meta.app_label,
                child_model._meta.model_name,
                name
            ),
            exc_info=True
        )


def get_relationship_url(parent_model, parent_field, child_model, **kwargs):
    logger = getLogger('podiant.api')
    opts = parent_model._meta
    name = 'api:%s_%s_%s_relationship' % (
        opts.app_label,
        opts.model_name,
        parent_field
    )

    try:
        return reverse(name, kwargs=kwargs)
    except NoReverseMatch:  # pragma: no cover
        logger.warning(
            (
                'No API endpoint found to return '
                'relationship between %s.%s and %s.%s (tried '
                'named URL pattern \'%s\')'
            ) % (
                opts.app_label,
                opts.model_name,
                child_model._meta.app_label,
                child_model._meta.model_name,
                name
            ),
            exc_info=True
        )


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

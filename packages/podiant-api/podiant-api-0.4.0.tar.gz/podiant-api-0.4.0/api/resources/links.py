from django.db.models import Model, QuerySet
from django.urls import reverse
from urllib.parse import parse_qs, urlencode
from ..exceptions import ConfigurationError


class ResourceLink(object):
    def __init__(self, obj, field=None, kind=None, page=None):
        from . import registry

        self.urlname = None
        self.kwargs = {}
        self.args = ()
        self.qs = {}

        if isinstance(obj, QuerySet):
            self.urlname = 'api:%s_%s_list' % (
                obj.model._meta.app_label,
                obj.model._meta.model_name
            )

            if page:
                self.qs['page'] = page

            return

        if isinstance(obj, Model):
            try:
                resource = registry.get(type(obj), 'detail')
            except KeyError:  # pragma: no cover
                raise ConfigurationError(
                    (
                        '%s.%s object cannot be linked to, as no API '
                        'resource exists'
                    ) % (
                        obj._meta.app_label,
                        obj._meta.model_name
                    )
                )

            if field is not None:
                field = obj._meta.get_field(field)
                self.urlname = 'api:%s_%s_%s' % (
                    obj._meta.app_label,
                    obj._meta.model_name,
                    field.name
                )

                if kind == 'relationship':
                    self.urlname += '_relationship'
                elif kind not in (None, 'relation'):  # pragma: no cover
                    raise ConfigurationError(
                        'Unknown link kind, \'%s\'' % kind
                    )

                id_value = getattr(obj, resource.pk_field)
                self.kwargs = {
                    resource.pk_field: id_value
                }

                return

            self.urlname = 'api:%s_%s_detail' % (
                obj._meta.app_label,
                obj._meta.model_name
            )

            id_value = getattr(obj, resource.pk_field)
            self.kwargs = {
                resource.pk_field: id_value
            }

            return

        raise ConfigurationError(  # pragma: no cover
            'Unable to determine how to create a link for given context'
        )

    def resolve(self, request):
        resolved = reverse(
            self.urlname,
            kwargs=self.kwargs
        )

        qs = parse_qs(request.META['QUERY_STRING'])
        qs.update(self.qs)

        if any(qs):
            qs = '?%s' % urlencode(qs, doseq=True)
        else:
            qs = ''

        absolute = request.build_absolute_uri(
            '%s%s' % (resolved, qs)
        )

        return absolute

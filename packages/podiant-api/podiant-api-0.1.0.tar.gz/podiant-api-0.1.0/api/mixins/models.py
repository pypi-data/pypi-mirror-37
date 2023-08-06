from collections import OrderedDict
from django.core.paginator import (
    Paginator, EmptyPage, InvalidPage, PageNotAnInteger
)

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.db.models import (
    Model, QuerySet, AutoField, DateField, DateTimeField, FileField,
    ManyToOneRel
)

from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.http.response import Http404
from django.forms.models import modelform_factory
from logging import getLogger
from urllib.parse import urlparse, urljoin, parse_qs, urlencode
from ..exceptions import (
    BadRequestError,
    UnprocessableEntityError,
    ConflictError,
    ConfigurationError
)

from .packing import PackingMixin
from .. import settings


class ModelMixin(PackingMixin):
    pk_field = 'pk'

    def get_order_by(self):
        if hasattr(self, 'order_by'):
            return self.order_by

        return (self.get_pk_field(),)

    def get_paginate_by(self):
        if hasattr(self, 'paginate_by'):
            return self.paginate_by

        return settings.DEFAULT_RPP

    def get_page_url(self, number):
        url = self.request.build_absolute_uri()
        urlparts = urlparse(url)
        qs = parse_qs(urlparts.query)
        qs['page'] = str(number)
        return urljoin(url, '?%s' % urlencode(qs))

    def get_fields(self):
        if hasattr(self, 'fields'):
            return self.fields

        return ()

    def get_relationships(self):
        if hasattr(self, 'relationships'):
            return self.relationships

        return ()

    def get_exclude(self):
        if hasattr(self, 'exclude'):
            return self.exclude

        return ()

    def get_read_only_fields(self):
        if hasattr(self, 'read_only_fields'):
            return self.read_only_fields

        return ()

    def get_pk_field(self):
        return self.pk_field

    def pack(self, obj, depth=0):
        links = {
            'self': self.request.build_absolute_uri()
        }

        logger = getLogger('podiant.api')

        if isinstance(obj, QuerySet):
            paginator = Paginator(obj, self.get_paginate_by())
            page_no = self.request.GET.get('page') or 1

            try:
                page = paginator.page(page_no)
            except PageNotAnInteger:
                raise BadRequestError('Invalid page number')
            except (InvalidPage, EmptyPage):
                raise Http404('No such page.')

            if page.has_next():
                links['next'] = self.get_page_url(page.next_page_number())
                links['last'] = self.get_page_url(paginator.num_pages)

            packed = [
                self.pack(o, depth=depth + 1)
                for o in page.object_list
            ]
        elif isinstance(obj, (list, tuple)):
            packed = [
                self.pack(o, depth=depth + 1)
                for o in obj
            ]
        elif isinstance(obj, Model):
            opts = obj._meta
            data = OrderedDict()
            rels = OrderedDict()

            fieldnames = [
                f.name
                for f in opts.get_fields()
            ]

            all_fields = self.get_fields()
            all_rels = self.get_relationships()
            all_exclude = self.get_exclude()
            pk_field = self.get_pk_field()

            for field in all_fields:
                if field not in fieldnames:  # pragma: no cover
                    raise ConfigurationError(
                        '\'%s\' field not present in %s model' % (
                            field,
                            opts.model_name
                        )
                    )

            for f in opts.get_fields():
                if any(all_fields) and f.name not in all_fields:
                    if any(all_rels) and f.name not in all_rels:
                        continue

                if any(all_exclude) and f.name in all_exclude:
                    continue

                if isinstance(f, AutoField):
                    continue

                if isinstance(f, (ForeignKey, ManyToOneRel, ManyToManyField)):
                    rel_url_name = 'api:%s_%s_%s' % (
                        opts.app_label,
                        opts.model_name,
                        f.name
                    )

                    try:
                        rel_url = self.request.build_absolute_uri(
                            reverse(
                                rel_url_name,
                                kwargs={
                                    pk_field: obj.pk
                                }
                            )
                        )
                    except NoReverseMatch:
                        logger.warning(
                            (
                                'No API endpoint found to return '
                                'relationship between %s.%s and %s.%s (tried '
                                'named URL pattern: "%s")'
                            ) % (
                                opts.app_label,
                                opts.model_name,
                                f.related_model._meta.app_label,
                                f.related_model._meta.model_name,
                                rel_url_name
                            ),
                            exc_info=True
                        )

                        rel_url = None

                    if isinstance(f, ForeignKey):
                        d = {
                            'type': '%s.%s' % (
                                f.related_model._meta.app_label,
                                f.related_model._meta.model_name
                            ),
                            'id': str(f.value_from_object(obj))
                        }
                    elif isinstance(f, (ManyToOneRel, ManyToManyField)):
                        d = [
                            {
                                'type': '%s.%s' % (
                                    f.related_model._meta.app_label,
                                    f.related_model._meta.model_name
                                ),
                                'id': str(i)
                            } for i in (
                                getattr(obj, f.name).values_list(
                                    'pk',
                                    flat=True
                                )
                            )
                        ]

                    rels[f.name] = {
                        'data': d
                    }

                    if rel_url:
                        rels[f.name]['links'] = {
                            'self': rel_url
                        }

                elif isinstance(f, ManyToManyField):
                    data[f.name] = f.value_from_object(obj)
                elif isinstance(f, (DateField, DateTimeField)):
                    v = f.value_from_object(obj)
                    data[f.name] = v and v.isoformat() or None
                elif isinstance(f, FileField):
                    v = f.value_from_object(obj)
                    data[f.name] = v and v.url or None
                else:
                    data[f.name] = self.pack(
                        f.value_from_object(obj),
                        depth=depth + 1
                    )

            packed = {
                'type': '%s.%s' % (
                    type(obj)._meta.app_label,
                    type(obj)._meta.model_name
                ),
                'id': str(getattr(obj, pk_field)),
                'attributes': data
            }

            if any(rels):
                packed['relationships'] = rels

            if isinstance(obj, self.model):
                detail_url_name = 'api:%s_%s_detail' % (
                    self.model._meta.app_label,
                    self.model._meta.model_name
                )

                try:
                    detail_url = self.request.build_absolute_uri(
                        reverse(
                            detail_url_name,
                            kwargs={
                                pk_field: obj.pk
                            }
                        )
                    )
                except NoReverseMatch:
                    logger.warning(
                        (
                            'No URL pattern found for %s.%s detail view ('
                            'tried %s)'
                        ) % (
                            self.model._meta.app_label,
                            self.model._meta.model_name,
                            detail_url_name
                        ),
                        exc_info=True
                    )
                else:
                    packed['links'] = {
                        'self': detail_url
                    }

                    links['self'] = detail_url
        elif isinstance(obj, Model):
            raise Exception(obj)
        else:
            packed = super().pack(obj, depth=depth)

        if depth == 0:
            return {
                'jsonapi': {
                    'version': '1.0'
                },
                'links': links,
                'data': packed
            }
        else:
            return packed

    def unpack(self, data):
        if 'data' not in data:
            raise UnprocessableEntityError('Missing data object.')

        kind_real = '%s.%s' % (
            self.model._meta.app_label,
            self.model._meta.model_name
        )

        if not isinstance(data, dict):
            raise UnprocessableEntityError(
                'A JSON object is required.'
            )

        data = data['data']
        if not isinstance(data, dict):
            raise UnprocessableEntityError(
                'data must be an object.'
            )

        if not data.get('type'):
            raise UnprocessableEntityError(
                'Missing object type.',
                {
                    'valid_types': [kind_real]
                }
            )

        kind = data['type']
        if kind != kind_real:
            raise ConflictError(
                'Invalid object type.',
                {
                    'specified': kind,
                    'valid_types': [kind_real]
                }
            )

        if self.request.method in ('PUT', 'PATCH'):
            if not data.get('id'):
                raise UnprocessableEntityError('Missing object ID.')

            obj = self.get_object()
            pk = data['id']
            pk_field = self.get_pk_field()
            pk_real = str(getattr(obj, pk_field))

            if str(pk) != pk_real:
                raise ConflictError(
                    'Invalid object ID.',
                    {
                        'specified': pk
                    }
                )

        attributes = data.get('attributes', {})
        rels = data.get('relationships', {})

        if not isinstance(attributes, dict):
            raise UnprocessableEntityError(
                'attributes must be an object.'
            )

        if not isinstance(rels, dict):
            raise UnprocessableEntityError(
                'relationships must be an object.'
            )

        final = dict(**attributes)
        opts = self.model._meta
        fieldnames = [
            f.name
            for f in opts.get_fields()
        ]

        for field, rel in rels.items():
            if field not in fieldnames:
                raise UnprocessableEntityError(
                    'Relationship does not exist.',
                    {
                        'relationship': field
                    }
                )

            db_field = opts.get_field(field)
            if rel.get('data') is None:
                raise UnprocessableEntityError(
                    'Relationship must have a data property.',
                    {
                        'relationship': field
                    }
                )

            rel_data = rel['data']

            if isinstance(rel_data, dict):
                rel_list = [rel_data]
            elif isinstance(rel_data, list):
                rel_list = rel_data
            else:
                raise UnprocessableEntityError(
                    'Relationship data must be an object or array.',
                    {
                        'relationship': field
                    }
                )

            rel_data_clean = []
            for rel_subdata in rel_list:
                rel_kind_real = '%s.%s' % (
                    db_field.related_model._meta.app_label,
                    db_field.related_model._meta.model_name
                )

                rel_kind = rel_subdata.get('type')
                if not rel_kind:
                    raise UnprocessableEntityError(
                        'Missing relationship object type.',
                        {
                            'relationship': field,
                            'valid_types': [rel_kind_real]
                        }
                    )

                if rel_kind != rel_kind_real:
                    raise ConflictError(
                        'Invalid relationship object type.',
                        {
                            'relationship': field,
                            'specified': rel_kind,
                            'valid_types': [rel_kind_real]
                        }
                    )

                rel_id = rel_subdata.get('id')
                if rel_id is None:
                    raise UnprocessableEntityError(
                        'Missing relationship object ID.',
                        {
                            'relationship': field
                        }
                    )

                rel_data_clean.append(rel_id)

            if isinstance(rel_data, dict):
                rel_data_clean = rel_data_clean[0]

            if rel_data_clean is not None:
                final[field] = rel_data_clean

        return final

    def get_queryset(self):
        return self.model.objects.order_by(*self.get_order_by())

    def get_form_fields(self):
        opts = self.model._meta
        fields = []
        all_fields = self.get_fields()
        all_rels = self.get_relationships()
        all_exclude = self.get_exclude()
        all_read_only = self.get_read_only_fields()

        for f in opts.get_fields():
            if any(all_fields) and f.name not in all_fields:
                if any(all_rels) and f.name not in all_rels:
                    continue

            if any(all_exclude) and f.name in all_exclude:
                continue

            if any(all_read_only) and f.name in all_read_only:
                continue

            if isinstance(f, AutoField) or f.name == self.get_pk_field():
                continue

            if isinstance(f, ManyToOneRel):
                continue

            if isinstance(f, DateField):
                if f.auto_now or f.auto_now_add:
                    continue

            fields.append(f.name)

        return fields

    def get_form_class(self, fields=None):
        all_fields = self.get_fields()
        all_exclude = self.get_exclude()

        if not hasattr(self, '_form_cache'):
            if hasattr(self, 'form_class'):
                self._form_cache = self.form_class
            elif not hasattr(self, 'model'):  # pragma: no cover
                raise ConfigurationError('Model not defined')
            else:
                if not any(
                    all_fields
                ) and not any(
                    all_exclude
                ):  # pragma: no cover
                    raise ConfigurationError(
                        (
                            'Neither a \'fields\' list nor an \'exclude\' '
                            'list has been defined'
                        )
                    )

                if fields is None:
                    f = self.get_form_fields()
                else:
                    f = fields

                self._form_cache = modelform_factory(
                    self.model,
                    fields=f
                )

        return self._form_cache

    def form_valid(self, form):
        return form.save()

    def get_object(self):
        if not hasattr(self, '_object_cache'):
            self._object_cache = self.model.objects.get(**self.kwargs)

        return self._object_cache

    def get_form_kwargs(self, form_class):
        kwargs = super().get_form_kwargs(form_class)
        pk_field = self.get_pk_field()

        if pk_field in self.kwargs:
            kwargs['instance'] = self.get_object()

        return kwargs

    def save(self, obj):
        data = self.get_initial()
        data.update(obj)
        form = self.get_form(data=data)

        if not form.is_valid():
            raise UnprocessableEntityError(
                'Object did not validate.',
                form.errors
            )

        obj = self.form_valid(form)
        return self.pack(obj)

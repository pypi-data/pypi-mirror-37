from collections import OrderedDict
from django.core.exceptions import FieldError
from django.core.paginator import (
    Paginator, EmptyPage, InvalidPage, PageNotAnInteger
)

from django.db.models import (
    Model, QuerySet, AutoField, DateField, DateTimeField, FileField,
    ManyToOneRel, ManyToManyRel
)

from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.http.response import Http404
from django.forms.models import modelform_factory
from urllib.parse import urlparse, urljoin, parse_qs, urlencode
from ..exceptions import (
    BadRequestError,
    UnprocessableEntityError,
    ConflictError,
    ConfigurationError
)

from ..filtering import qs_name_to_kwarg
from ..utils import (
    get_object_url,
    get_object_id,
    get_id_field,
    get_type_name,
    get_relation_url,
    get_relationship_url,
    urlise_field_name,
    unurlise_field_name
)

from .. import settings
from .packing import PackingMixin
import re


class ModelMixin(PackingMixin):
    pk_field = 'pk'

    def get_order_by(self):
        if self.request.GET.get('sort'):
            sort = [
                s.strip().replace('.', '__')
                for s in self.request.GET['sort'].split(',')
                if s and s.strip()
            ]

            if any(sort):
                return tuple(set(sort))

        return getattr(self, 'order_by', None) or (self.get_pk_field(),)

    def get_paginate_by(self):
        return getattr(self, 'paginate_by', settings.DEFAULT_RPP)

    def get_page_url(self, number):
        url = self.request.build_absolute_uri()
        urlparts = urlparse(url)
        qs = parse_qs(urlparts.query)
        qs['page'] = str(number)
        return urljoin(url, '?%s' % urlencode(qs, doseq=True))

    def get_fields(self):
        return getattr(self, 'fields', ())

    def get_relationships(self):
        return getattr(self, 'relationships', ())

    def get_exclude(self):
        return getattr(self, 'exclude', ())

    def get_readonly_fields(self):
        return getattr(self, 'readonly_fields', ())

    def get_pk_field(self):
        return self.pk_field

    def pack(self, obj, depth=0):
        links = {
            'self': self.request.build_absolute_uri()
        }

        if isinstance(obj, QuerySet):
            paginator = Paginator(obj, self.get_paginate_by())
            page_no = self.request.GET.get('page') or 1

            try:
                page = paginator.page(page_no)
            except PageNotAnInteger:
                raise BadRequestError('Invalid page number.')
            except (InvalidPage, EmptyPage):
                raise Http404('No such page.')

            links['first'] = self.get_page_url(1)
            links['prev'] = None
            links['next'] = None
            links['last'] = self.get_page_url(1)

            if page.has_next():
                links['next'] = self.get_page_url(page.next_page_number())
                links['last'] = self.get_page_url(paginator.num_pages)

            if page.has_previous():
                links['prev'] = self.get_page_url(page.previous_page_number())

            packed = [
                self.pack(o, depth=depth + 1)
                for o in page.object_list
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
                url_friendly_field_name = urlise_field_name(f.name)

                if any(all_fields) and f.name not in all_fields:
                    if any(all_rels) and f.name not in all_rels:
                        continue

                if any(all_exclude) and f.name in all_exclude:
                    continue

                if isinstance(f, AutoField):
                    continue

                if isinstance(f, ForeignKey):
                    relation_url = get_relation_url(
                        parent_model=type(obj),
                        parent_field=f.name,
                        child_model=f.related_model,
                        **{
                            pk_field: get_object_id(obj)
                        }
                    )

                    relationship_url = get_relationship_url(
                        parent_model=type(obj),
                        parent_field=f.name,
                        child_model=f.related_model,
                        **{
                            pk_field: get_object_id(obj)
                        }
                    )

                    if relation_url and relationship_url:
                        rels[url_friendly_field_name] = {
                            'links': {
                                'self': self.request.build_absolute_uri(
                                    relationship_url
                                ),
                                'related': self.request.build_absolute_uri(
                                    relation_url
                                )
                            },
                            'data': {
                                'type': get_type_name(f.related_model),
                                'id': get_object_id(getattr(obj, f.name))
                            }
                        }

                    continue

                if isinstance(f, (ManyToOneRel, ManyToManyField, ManyToManyRel)):
                    relation_url = get_relation_url(
                        parent_model=type(obj),
                        parent_field=f.name,
                        child_model=f.related_model,
                        **{
                            pk_field: get_object_id(obj)
                        }
                    )

                    relationship_url = get_relationship_url(
                        parent_model=type(obj),
                        parent_field=f.name,
                        child_model=f.related_model,
                        **{
                            pk_field: get_object_id(obj)
                        }
                    )

                    if relation_url and relationship_url:
                        rels[url_friendly_field_name] = {
                            'links': {
                                'self': self.request.build_absolute_uri(
                                    relationship_url
                                ),
                                'related': self.request.build_absolute_uri(
                                    relation_url
                                )
                            }
                        }

                    continue

                if isinstance(f, (DateField, DateTimeField)):
                    v = f.value_from_object(obj)
                    data[url_friendly_field_name] = v and v.isoformat() or None
                    continue

                if isinstance(f, FileField):
                    v = f.value_from_object(obj)
                    data[url_friendly_field_name] = v and v.url or None
                    continue

                data[url_friendly_field_name] = self.pack(
                    f.value_from_object(obj),
                    depth=depth + 1
                )

            packed = {
                'type': get_type_name(obj),
                'id': get_object_id(obj),
                'attributes': data
            }

            if any(rels):
                packed['relationships'] = rels

            if isinstance(obj, self.model):
                detail_url = get_object_url(obj)

                if detail_url:
                    detail_url = self.request.build_absolute_uri(detail_url)
                    packed['links'] = {
                        'self': detail_url
                    }

                    links['self'] = detail_url
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
        if not isinstance(data, dict):
            raise UnprocessableEntityError(
                'A JSON object is required.'
            )

        if 'data' not in data:
            raise UnprocessableEntityError('Missing data object.')

        kind_real = get_type_name(self.model)
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

        final = dict(
            [
                (
                    unurlise_field_name(key),
                    value
                ) for (
                    key,
                    value
                ) in data.get('attributes', {}).items()
            ]
        )

        opts = self.model._meta
        fieldnames = [
            f.name
            for f in opts.get_fields()
        ]

        for (
            field, rel
        ) in [
            (
                unurlise_field_name(f),
                r
            ) for (f, r) in rels.items()
        ]:
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
                rel_kind_real = get_type_name(db_field.related_model)
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

    def get_filter(self):
        kwargs = {}

        for key in self.request.GET.keys():
            match = re.match(r'^filter\[([\w\.-]+)\]$', key)
            if match is None:
                continue

            for field in match.groups():
                f = qs_name_to_kwarg(field, self.model._meta)
                kwargs['%s' % f] = self.request.GET[key]

        return kwargs

    def get_queryset(self):
        return self.model.objects.filter(
            **self.get_filter()
        ).order_by(
            *self.get_order_by()
        )

    def get_form_fields(self):
        opts = self.model._meta
        fields = []
        all_fields = self.get_fields()
        all_rels = self.get_relationships()
        all_exclude = self.get_exclude()
        all_read_only = self.get_readonly_fields()

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

            if isinstance(f, (ManyToOneRel, ManyToManyRel)):
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

                try:
                    self._form_cache = modelform_factory(
                        self.model,
                        fields=f
                    )
                except FieldError as ex:
                    raise UnprocessableEntityError(str(ex))

        return self._form_cache

    def form_valid(self, form):
        return form.save()

    def get_object(self):
        if not hasattr(self, '_object_cache'):
            self._object_cache = self.model.objects.get(**self.kwargs)

        return self._object_cache

    def get_initial(self):
        return {}

    def get_form_kwargs(self, form_class):
        kwargs = {}
        pk_field = self.get_pk_field()

        if pk_field in self.kwargs:
            kwargs['instance'] = self.get_object()

        return kwargs

    def patch_form_fields(self, form):
        for name, field in form.fields.items():
            if isinstance(field, (ModelChoiceField, ModelMultipleChoiceField)):
                field.to_field_name = get_id_field(field.queryset.model)

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        kw = self.get_form_kwargs(form_class)
        kw.update(kwargs)
        form = form_class(**kw)
        self.patch_form_fields(form)

        return form

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

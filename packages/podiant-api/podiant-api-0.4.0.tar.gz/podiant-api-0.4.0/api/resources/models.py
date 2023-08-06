from collections import OrderedDict
from django.core.exceptions import FieldError
from django.core.paginator import (
    Paginator, EmptyPage, InvalidPage, PageNotAnInteger
)

from django.db.models import (
    AutoField,
    DateField,
    DateTimeField,
    FileField,
    ManyToManyRel,
    ManyToOneRel
)

from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.models import modelform_factory
from django.http.response import Http404
from ..exceptions import (
    BadRequestError,
    ConfigurationError,
    ConflictError,
    UnprocessableEntityError
)

from ..utils import (
    get_object_id,
    get_type_name,
    urlise_field_name,
    unurlise_field_name
)

from .base import ResourceDetailBase, ResourceListBase


class ModelMixin(object):
    """
    This class contains properties and methods common to both model resources
    and model resource lists.
    """

    pk_field = 'pk'

    def get_fields(self):
        """
        This method returns the value of the `fields` property if specified.
        Otherwise it returns an empty tuple. It is used to define the fields
        that should be returned as part of the `attributes` dictionary for a
        resource object.
        """

        return getattr(self, 'fields', ())

    def get_relationships(self):
        """
        This method returns the value of the `relationships` property if
        specified. Otherwise it returns an empty tuple. It is used to define
        the contents of the `relationthips` dictionary for a resource object.
        """

        return getattr(self, 'relationships', ())

    def get_exclude(self):
        """
        This method returns the value of the `exclude` property if specified.
        Otherwise it returns an empty tuple. It is used to define the fields
        that should not be included in the `attributes` dictionary of a
        resource object.
        """

        return getattr(self, 'exclude', ())

    def get_readonly_fields(self):
        """
        This method returns the value of the `readonly_fields` property if
        specified. Otherwise it returns an empty tuple. It is used to define
        the fields that a user cannot change via the API.
        """

        return getattr(self, 'readonly_fields', ())

    def get_pk_field(self):
        """
        Returns the value of the `pk_field` property. Usually this is the `pk`
        property of a model.
        """

        return self.pk_field

    def get_only(self):
        """
        Returns a list of local model field names that should be included in a
        queryset.
        """

        rels = self.get_relationships()
        return [
            field for field in self.get_fields()
            if field not in rels
        ]

    def get_defer(self):
        """
        Returns a list of local model field names that should be excluded from
        a queryset by default.
        """

        rels = self.get_relationships()
        return [
            field for field in self.get_exclude()
            if field not in rels
        ]

    def get_prefetch_related(self, include):
        """
        Returns a list of related field names (such as many-to-many
        relationships) that should be prefetched, as they have been specially
        requested via the `include` uerystring parameter.
        """

        rels = self.get_relationships()
        prefetch = []
        includes = self.get_include()

        for field in [
            self.model._meta.get_field(field)
            for field in rels if field in includes
        ]:
            if isinstance(field, (ManyToManyField, ManyToOneRel)):
                prefetch.append(field.name)

        return prefetch

    def get_queryset(self):
        """
        Returns a Djagno queryset, filtered as requested by the API user,
        containing only the fields specified by the resource schema, and
        pre-fetching any necessary many-to-many or many-to-one relationships
        explicitly requested in the `include` querystring parameter.
        """

        filter = self.kwargs.get('filter', None)
        include = self.kwargs.get('include', None)
        order_by = self.kwargs.get('order_by', None)

        queryset = self.model.objects.select_related().only(
            *self.get_only()
        ).defer(
            *self.get_defer()
        )

        if isinstance(filter, dict):
            queryset = queryset.filter(**filter)

        if isinstance(include, (list, tuple)):
            queryset = queryset.prefetch_related(
                *self.get_prefetch_related(include)
            )

        if isinstance(order_by, (list, tuple)) and any(order_by):
            queryset = queryset.order_by(*order_by)
        else:
            queryset = queryset.order_by(
                self.get_pk_field()
            )

        return queryset

    def _extract_jsonapi_data(self, data):
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

        return data

    def unpack(self, data):
        """
        A public interface to two private methods, that check the validity of
        the data and then unpack it to a dictionary.
        """

        data = self._extract_jsonapi_data(data)
        return self._unpack(data)

    def _unpack(self, data):
        """
        Given a dictionary conforming to the JSON-API spec, this method returns
        a dictionary that should be passed to a form as the `data` argument, in
        order to save the resource object as a model instance. It performs a
        number of validation steps, raising various 4xx HTTP errors upon
        finding data that doesn't conform to the spec.
        """

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

    def get_form_fields(self):
        """
        This method returns a list of field names that should be passed to the
        model form factory, if no explicit form class has been defined for this
        resource. Fields that have automatically-set values or that should
        otherwise not work within a model form context, are ignored.
        """

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

    def get_form_kwargs(self, form_class):
        """
        Returns the keyword arguments passed to a form class's init method.
        """

        kwargs = super().get_form_kwargs(form_class)
        pk_field = self.get_pk_field()

        if pk_field in self.kwargs:
            kwargs['instance'] = self.get_object()

        return kwargs

    def get_form_class(self, fields=None):
        """
        This method returns a runtime-generated model class for this model's
        local fields and relationships. If the optional `fields` argument is
        passed in, only the fields specified in that list will be included in
        the form. This is useful when performing PATCH operations, as only the
        fields that are being updated will be validated.
        """

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
        """
        Given a model form, this method saves the form's data. It is typically
        called in POST, PUT and PATCH operations, and can be overridden to
        perform extra operations before the object is saved.
        """

        return form.save()


class ModelResource(ModelMixin, ResourceDetailBase):
    def get_object(self):
        """
        Returns a single object from the model queryset that also matches
        the filter expression passed in via kwargs.
        """

        if not hasattr(self, '_object_cache'):
            if hasattr(self, 'object'):
                self._object_cache = self.object
            elif 'object' in self.kwargs:
                self._object_cache = self.kwargs['object']
            elif not any(self.kwargs.get('object_kwargs', {})):
                raise ConfigurationError(
                    'No object_kwargs defined. These are necessary to '
                    'determine how to find a single object, since objects '
                    'are not always found via their primary key'
                )
            else:
                self._object_cache = self.get_queryset().get(
                    **self.kwargs['object_kwargs']
                )

        return self._object_cache

    def pack(self, depth=0):
        """
        This method, given a model instance, returns a JSON-API representation
        of that instance, as a resource object.
        """

        obj = self.get_object()
        links = {
            'self': self.link(obj)
        }

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
                relation_url = self.link(obj, f.name)
                relationship_url = self.link(obj, f.name, 'relationship')

                if relation_url and relationship_url:
                    rels[url_friendly_field_name] = {
                        'links': {
                            'self': relationship_url,
                            'related': relation_url
                        },
                        'data': {
                            'type': get_type_name(f.related_model),
                            'id': get_object_id(getattr(obj, f.name))
                        }
                    }

                continue

            if isinstance(f, (ManyToOneRel, ManyToManyField, ManyToManyRel)):
                relation_url = self.link(obj, f.name)
                relationship_url = self.link(obj, f.name, 'relationship')

                if relation_url and relationship_url:
                    rels[url_friendly_field_name] = {
                        'links': {
                            'self': relationship_url,
                            'related': relation_url
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

            data[url_friendly_field_name] = f.value_from_object(obj)

        packed = {
            'type': get_type_name(obj),
            'id': get_object_id(obj),
            'attributes': data
        }

        if any(rels):
            packed['relationships'] = rels

        detail_url = self.link(obj)
        packed['links'] = {
            'self': detail_url
        }

        links['self'] = detail_url

        if depth == 0:
            packed = {
                'jsonapi': {
                    'version': '1.0'
                },
                'links': links,
                'data': packed
            }

        return packed

    def unpack(self, data):
        """
        A public interface to the validation and unpacking methods. Sandwiched
        in-between those calls is a check that the data object carries an
        appropriate ID for updating.
        """

        data = self._extract_jsonapi_data(data)

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

        return self._unpack(data)


class ModelResourceList(ModelMixin, ResourceListBase):
    def get_objects(self):
        return self.get_queryset()

    def pack(self, depth=0):
        """
        Given a collection of objects, this method returns a JSON-API
        representation of the list, paginated.
        """

        from . import registry

        page_no = self.kwargs.get('page', None)
        rpp = self.kwargs.get('rpp', None)
        obj = self.get_objects()

        links = {
            'self': self.link(obj)
        }

        resource_class = registry.get(self.model, 'detail')
        if page_no is not None and rpp is not None:
            paginator = Paginator(obj, rpp)

            try:
                page = paginator.page(page_no)
            except PageNotAnInteger:
                raise BadRequestError('Invalid page number.')
            except (InvalidPage, EmptyPage):
                raise Http404('No such page.')

            links.update(
                {
                    'first': self.link(obj, page=1),
                    'prev': None,
                    'next': None,
                    'last': self.link(obj, page=1)
                }
            )

            if page.has_next():
                links['next'] = self.link(obj, page=page.next_page_number())
                links['last'] = self.link(obj, page=paginator.num_pages)

            if page.has_previous():
                links['prev'] = self.link(obj, page=page.previous_page_number())

            packed = [
                resource_class(object=o).pack(depth=depth + 1)
                for o in page.object_list
            ]
        else:
            packed = [
                resource_class(object=o).pack(depth=depth + 1)
                for o in obj
            ]

        if depth == 0:
            packed = {
                'jsonapi': {
                    'version': '1.0'
                },
                'links': links,
                'data': packed
            }

        return packed

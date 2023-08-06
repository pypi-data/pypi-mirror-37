from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import FieldError
from django.db import transaction
from django.db.models import ForeignKey, ManyToOneRel, ManyToManyField
from django.http.response import HttpResponse
from django.views.generic.base import View
from ..authorisation import AuthBundle
from ..decorators import jsonapi
from ..exceptions import (
    MethodNotAllowedError, ConfigurationError, UnprocessableEntityError
)

from ..filtering import qs_name_to_kwarg
from ..mixins import (
    ModelMixin,
    JSONMixin,
    AuthenticationMixin,
    AuthorisationMixin
)

from ..utils import (
    get_id_field,
    get_object_id,
    get_type_name
)

from ..resources import registry
from .. import settings
import re


class ModelViewBase(
    ModelMixin,
    JSONMixin,
    AuthenticationMixin,
    AuthorisationMixin,
    View
):
    def get_filter(self):
        """
        This method looks for querystring parameters that follow the
        `filter[<field>]` pattern, and atetmpts to turn the filter expression
        into a Django query expression, expressed as a dictionary that can
        then be applied via a Django query's kwargs.
        """

        kwargs = {}

        for key in self.request.GET.keys():
            match = re.match(r'^filter\[([\w\.-]+)\]$', key)
            if match is None:
                continue

            for field in match.groups():
                f = qs_name_to_kwarg(field, self.model._meta)
                kwargs[f] = self.request.GET[key]

        return kwargs

    def get_include(self):
        """
        Given a request with an `include` querystring parameter, returns a
        list of model field names that can be found in that list. If a field
        has been requested that can't be found, an `UnprocessableEntityError`
        exception is raised.
        """

        includes = []

        for name in [
            name.strip()
            for name in self.request.GET.get('include', '').split(',')
            if name and name.strip()
        ]:
            try:
                field = self.model._meta.get_field(name)
            except FieldError as ex:
                raise UnprocessableEntityError(str(ex))
            else:
                includes.append(field.name)

        return includes

    def get_order_by(self):
        """
        If specified by querystring, this method returns the field names
        requested. If an `order_by` property is declared, this is used as a
        fallback, and finally if no ordering can be determined, the field used
        as the identifier (usually teh primary key field) is returned.
        """

        if self.request.GET.get('sort'):
            sort = [
                s.strip().replace('.', '__')
                for s in self.request.GET['sort'].split(',')
                if s and s.strip()
            ]

            if any(sort):
                return tuple(set(sort))

        return getattr(self, 'order_by', [])

    def get_paginate_by(self):
        """
        Returns the number of records that should be in a paginated list.
        If a `paginate_by` property is specified, its value is used, otherwise
        it's taken from the default `API_DEFAULT_RPP` setting.
        """

        return getattr(self, 'paginate_by', settings.DEFAULT_RPP)

    def get_auth_bundle_data(self):
        return {}

    def get_auth_bundle(self, context):
        return AuthBundle(context, **self.get_auth_bundle_data())

    def precheck(self, request, context):
        method = request.method.lower()
        if method == 'head':
            method = 'get'

        if not hasattr(self, method):
            raise MethodNotAllowedError('Method not allowed.')

        authenticated = False
        for authenticator in self.get_authenticators():
            if authenticator.authenticate(request) is True:
                authenticated = True
                break

        if not authenticated:
            request.user = AnonymousUser()

        bundle = self.get_auth_bundle(context)
        for authoriser in self.get_authorisers():
            authoriser.authorise(request, bundle)

    def form_valid(self, form):
        resource = self.get_resource()
        return resource.form_valid(form)


class ListView(ModelViewBase):
    @jsonapi()
    def dispatch(self, request, *args, **kwargs):
        self.precheck(request, 'list')

        if request.method in ('HEAD', 'GET'):
            return self.respond(
                self.get(request)
            )

        if request.method == 'POST':
            data = self.post(request)
            response = self.respond(data)

            if response.status_code == 200:
                response.status_code = 201
                response['Location'] = data['links']['self'].resolve(request)

            return response

    def get_resource_kwargs(self):
        filter = self.get_filter()
        include = self.get_include()
        order_by = self.get_order_by()
        paginate_by = self.get_paginate_by()
        kwargs = {}

        if any(filter):
            kwargs['filter'] = filter

        if any(include):
            kwargs['include'] = include

        if any(order_by):
            kwargs['order_by'] = order_by

        if paginate_by is not None:
            kwargs['rpp'] = paginate_by
            kwargs['page'] = self.request.GET.get('page', '1')

        return kwargs

    def get(self, request):
        return self.get_resource().pack()

    def post(self, request):
        data = self.deserialise(request.body)
        resource = self.get_resource()
        unpacked = resource.unpack(data)
        form = resource.get_form(data=unpacked)
        self.patch_form_fields(form)

        if not form.is_valid():
            raise UnprocessableEntityError(
                'Object did not validate.',
                form.errors
            )

        obj = self.form_valid(form)
        resource_class = registry.get(type(obj), 'detail')
        resource = resource_class(object=obj)
        return resource.pack()


class DetailView(ModelViewBase):
    @jsonapi()
    def dispatch(self, request, *args, **kwargs):
        self.precheck(request, 'detail')

        if request.method in ('HEAD', 'GET'):
            return self.respond(
                self.get(request)
            )

        if request.method == 'PATCH':
            return self.respond(
                self.patch(request)
            )

        if request.method == 'PUT':
            return self.respond(
                self.put(request)
            )

        if request.method == 'DELETE':
            return self.delete(request)

    def get_resource_kwargs(self):
        include = self.get_include()
        kwargs = {
            'object_kwargs': self.kwargs
        }

        if any(include):
            kwargs['include'] = include

        return kwargs

    def get_auth_bundle_data(self):
        data = super().get_auth_bundle_data()
        data['object'] = self.get_resource().get_object()

        return data

    def get(self, request, **kwargs):
        return self.get_resource().pack()

    def patch(self, request):
        data = self.deserialise(request.body)
        resource = self.get_resource()
        unpacked = resource.unpack(dict(**data))

        form_class = resource.get_form_class(fields=unpacked.keys())
        kw = resource.get_form_kwargs(form_class)
        kw['instance'] = resource.get_object()
        kw['data'] = unpacked
        form = form_class(**kw)
        self.patch_form_fields(form)

        if not form.is_valid():
            raise UnprocessableEntityError(
                'Object did not validate.',
                form.errors
            )

        resource.object = self.form_valid(form)
        return resource.pack()

    def put(self, request):
        data = self.deserialise(request.body)
        resource = self.get_resource()
        unpacked = resource.unpack(dict(**data))
        form = resource.get_form(
            data=unpacked,
            instance=resource.get_object()
        )

        self.patch_form_fields(form)

        if not form.is_valid():
            raise UnprocessableEntityError(
                'Object did not validate.',
                form.errors
            )

        resource.object = self.form_valid(form)
        return resource.pack()

    def delete(self, request):
        self.get_resource().get_object().delete()
        return HttpResponse(
            status=204,
            content_type='application/vnd.api+json'
        )


class RelationView(ModelViewBase):
    def get_resource_kwargs(self):
        include = self.get_include()
        kwargs = {
            'object_kwargs': self.kwargs
        }

        if any(include):
            kwargs['include'] = include

        return kwargs

    @jsonapi()
    def get(self, request, **kwargs):
        self.precheck(request, 'detail')
        resource = self.get_resource()
        obj = resource.get_object()
        field = self.model._meta.get_field(self.rel)

        if field is None:  # pragma: no cover
            raise ConfigurationError(
                '\'%s\' field not found in \'%s.%s\' model' % (
                    self.rel,
                    self.model._meta.app_label,
                    self.model._meta.model_name
                )
            )

        if isinstance(field, (ManyToOneRel, ManyToManyField)):
            context = 'list'
            subresource_kwargs = {
                'filter': {
                    'pk__in': getattr(obj, field.name).values_list(
                        'pk',
                        flat=True
                    )
                }
            }
        else:
            context = 'detail'
            subresource_kwargs = {
                'object_kwargs': {
                    'pk': field.value_from_object(obj)
                }
            }

        subresource_class = registry.get(
            field.related_model,
            context
        )

        subresource = subresource_class(**subresource_kwargs)

        return self.respond(
            subresource.pack()
        )


class RelationshipView(ModelViewBase):
    def get_resource_kwargs(self):
        include = self.get_include()
        kwargs = {
            'object_kwargs': self.kwargs
        }

        if any(include):
            kwargs['include'] = include

        return kwargs

    @jsonapi()
    def get(self, request, **kwargs):
        self.precheck(request, 'detail')

        resource = self.get_resource()
        obj = resource.get_object()
        field = self.model._meta.get_field(self.rel)

        if field is None:  # pragma: no cover
            raise ConfigurationError(
                '\'%s\' field not found in \'%s.%s\' model' % (
                    self.rel,
                    self.model._meta.app_label,
                    self.model._meta.model_name
                )
            )

        subobj = getattr(obj, field.name)
        if isinstance(field, ForeignKey):
            data = {
                'id': get_object_id(subobj),
                'type': get_type_name(subobj)
            }
        elif isinstance(field, (ManyToOneRel, ManyToManyField)):
            type_name = get_type_name(field.related_model)
            data = [
                {
                    'id': pk,
                    'type': type_name
                } for pk in subobj.values_list(
                    get_id_field(field.related_model),
                    flat=True
                )
            ]
        else:  # pragma: no cover
            raise ConfigurationError('Unsupported relationship')

        rel_url = resource.link(obj)
        packed = {
            'links': {
                'self': self.request.build_absolute_uri()
            },
            'data': data
        }

        if rel_url:
            packed['links']['related'] = rel_url

        return self.respond(packed)


def modelmixin_factory(
    Model, prepopulated_fields={},
    authenticators=None, authorisers=None
):
    opts = Model._meta
    attrs = {
        'model': Model
    }

    if authenticators is not None:
        attrs['authenticators'] = authenticators

    if authorisers is not None:
        attrs['authorisers'] = authorisers

    class mixin(object):
        @transaction.atomic()
        def form_valid(self, form):
            if self.request.method in ('PUT', 'PATCH') or not any(
                prepopulated_fields
            ):
                return super().form_valid(form)

            obj = form.save(commit=False)
            for key, expression in prepopulated_fields.items():
                if opts.get_field(key) is None:  # pragma: no cover
                    raise ConfigurationError(
                        '\'%s\' field not present in %s model' % (
                            key,
                            opts.model_name
                        )
                    )

                value = expression(self.request)
                setattr(obj, key, value)

            obj.save()
            form.save_m2m()

            return obj

    return type(
        '%sMixin' % Model.__name__,
        (mixin,),
        attrs
    )


def relationmixin_factory(ParenetModel, name):
    attrs = {
        'model': ParenetModel,
        'rel': name
    }

    return type(
        '%sRelationMixin' % ParenetModel.__name__,
        (),
        attrs
    )


def relationshipmixin_factory(ParenetModel, name):
    attrs = {
        'model': ParenetModel,
        'rel': name
    }

    return type(
        '%sRelationshipMixin' % ParenetModel.__name__,
        (),
        attrs
    )

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import ManyToOneRel, ManyToManyField
from django.http.response import HttpResponse
from django.views.generic.base import View
from ..decorators import jsonapi
from ..exceptions import (
    MethodNotAllowedError, ConfigurationError, UnprocessableEntityError
)

from ..mixins import (
    ModelMixin,
    JSONMixin,
    AuthenticationMixin,
    AuthorisationMixin
)


class ModelViewBase(
    ModelMixin,
    JSONMixin,
    AuthenticationMixin,
    AuthorisationMixin,
    View
):
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

        for authoriser in self.get_authorisers():
            authoriser.authorise(request, context)


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
                response['Location'] = data['links']['self']

            return response

    def get(self, request):
        return self.pack(self.get_queryset())

    def post(self, request):
        data = self.deserialise(request.body)
        unpacked = self.unpack(data)
        return self.save(unpacked)


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

    def get(self, request, **kwargs):
        return self.pack(self.get_object())

    def patch(self, request):
        data = self.deserialise(request.body)
        unpacked = self.unpack(dict(**data))

        data = self.get_initial()
        data.update(unpacked)

        form_class = self.get_form_class(fields=unpacked.keys())
        kw = self.get_form_kwargs(form_class)
        kw['data'] = data
        form = form_class(**kw)

        if not form.is_valid():
            raise UnprocessableEntityError(
                'Object did not validate.',
                form.errors
            )

        obj = self.form_valid(form)
        return self.pack(obj)

    def put(self, request):
        data = self.deserialise(request.body)
        unpacked = self.unpack(dict(**data))
        return self.save(unpacked)

    def delete(self, request):
        self.get_object().delete()
        return HttpResponse(
            status=204,
            content_type='application/vnd.api+json'
        )


class RelationView(ModelViewBase):
    @jsonapi()
    def get(self, request, **kwargs):
        self.precheck(request, 'detail')

        obj = self.get_object()
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
            return self.respond(
                self.pack(
                    getattr(obj, field.name).order_by(
                        *self.get_order_by()
                    )
                )
            )

        subobj = getattr(obj, field.name)
        return self.respond(
            self.pack(subobj)
        )


class RelationshipView(ModelViewBase):
    def get_fields(self):
        return [self.get_pk_field()]

    @jsonapi()
    def get(self, request, **kwargs):
        self.precheck(request, 'detail')

        obj = self.get_object()
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
            return self.respond(
                self.pack(
                    getattr(obj, field.name).only(
                        *self.get_fields()
                    ).order_by(
                        *self.get_order_by()
                    )
                )
            )

        pk = field.value_from_object(obj)
        for subobj in field.related_model.objects.only(
            *self.get_fields()
        ).filter(pk=pk):
            return self.respond(
                self.pack(subobj)
            )

        return self.respond({})


def modelmixin_factory(
    Model, order_by=None, fields=None, exclude=None, form_class=None,
    readonly_fields=None, pk_field='pk', prepopulated_fields={},
    paginate_by=None, relationships=(), authoriser=None
):
    opts = Model._meta
    attrs = {
        'model': Model,
        'relationships': relationships,
        'pk_field': pk_field
    }

    if order_by is not None:
        attrs['order_by'] = order_by

    if authoriser is not None:
        attrs['authorisers'] = [authoriser]

    if fields is not None:
        attrs['fields'] = fields

    if exclude is not None:
        attrs['exclude'] = exclude

    if form_class is not None:
        attrs['form_class'] = form_class

    if readonly_fields is not None and any(readonly_fields):
        attrs['readonly_fields'] = readonly_fields

    if paginate_by is not None:
        attrs['paginate_by'] = paginate_by

    class mixin(object):
        @transaction.atomic()
        def form_valid(self, form):
            if not any(prepopulated_fields):
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


def relationmixin_factory(
    ParenetModel, name, fields=(), exclude=(), pk_field='pk',
    paginate_by=None
):
    attrs = {
        'model': ParenetModel,
        'rel': name,
        'pk_field': pk_field
    }

    if fields is not None:
        attrs['fields'] = fields

    if exclude is not None:
        attrs['exclude'] = exclude

    if paginate_by is not None:
        attrs['paginate_by'] = paginate_by

    return type(
        '%sRelationMixin' % ParenetModel.__name__,
        (),
        attrs
    )


def relationshipmixin_factory(ParenetModel, name, pk_field='pk'):
    attrs = {
        'model': ParenetModel,
        'rel': name,
        'pk_field': pk_field
    }

    return type(
        '%sRelationshipMixin' % ParenetModel.__name__,
        (),
        attrs
    )

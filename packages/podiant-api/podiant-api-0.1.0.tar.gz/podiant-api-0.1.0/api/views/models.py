from django.db import transaction
from django.db.models import ManyToOneRel
from django.http.response import HttpResponse
from django.views.generic.base import View
from ..decorators import handle_exceptions
from ..exceptions import (
    MethodNotAllowedError, ConfigurationError, UnprocessableEntityError
)

from ..mixins import ModelMixin, JSONMixin, AuthorisationMixin


class ModelViewBase(ModelMixin, JSONMixin, AuthorisationMixin, View):
    pass


class ListView(ModelViewBase):
    @handle_exceptions()
    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if method == 'head':
            method = 'get'

        if not hasattr(self, method):
            raise MethodNotAllowedError('Method not allowed.')

        for authoriser in self.get_authorisers():
            authoriser.authorise(request, 'list')

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
        unpacked = self.unpack(dict(**data))
        return self.save(unpacked)


class DetailView(ModelViewBase):
    @handle_exceptions()
    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if method == 'head':
            method = 'get'

        if not hasattr(self, method):
            raise MethodNotAllowedError('Method not allowed.')

        for authoriser in self.get_authorisers():
            authoriser.authorise(request, 'detail')

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
            content_type='application/json'
        )


class RelationshipView(ModelViewBase):
    @handle_exceptions()
    def get(self, request, **kwargs):
        for authoriser in self.get_authorisers():
            authoriser.authorise(request, 'list')

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

        subobj = getattr(obj, field.name)
        if isinstance(field, ManyToOneRel):
            return self.respond(
                self.pack(
                    getattr(obj, field.name).all()
                )
            )

        return self.respond(
            self.pack(subobj)
        )


def modelmixin_factory(
    Model, order_by=None, fields=None, exclude=None, read_only_fields=None,
    pk_field='pk', prepopulated_fields={}, paginate_by=None, relationships=(),
    authoriser=None
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

    if read_only_fields is not None:
        attrs['read_only_fields'] = read_only_fields

    if paginate_by is not None:
        attrs['paginate_by'] = paginate_by

    class mixin(object):
        @transaction.atomic()
        def form_valid(self, form):
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
        '%sRelationshipMixin' % ParenetModel.__name__,
        (),
        attrs
    )

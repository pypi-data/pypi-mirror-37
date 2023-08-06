from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .exceptions import ConfigurationError
from .utils import get_type_name
from .views.models import (
    modelmixin_factory, ListView, DetailView,
    relationmixin_factory, relationshipmixin_factory,
    RelationView, RelationshipView
)


def rest(Model, **kwargs):
    order_by = kwargs.pop('order_by', None)
    fields = kwargs.pop('fields', None)
    exclude = kwargs.pop('exclude', None)
    readonly_fields = kwargs.pop('readonly_fields', None)
    form_class = kwargs.pop('form_class', None)
    prepopulated_fields = kwargs.pop('prepopulated_fields', None)
    pk_field = kwargs.pop('pk_field', None)
    paginate_by = kwargs.pop('paginate_by', None)
    relations = kwargs.pop('relations', {})
    authorisers = kwargs.pop('authorisers', None)
    authenticators = kwargs.pop('authenticators', None)
    opts = Model._meta
    slug = get_type_name(Model)

    for key in kwargs.keys():  # pragma: no cover
        raise TypeError(
            'rest() got an unexpected keyword argument \'%s\'' % key
        )

    urlpatterns = []
    kw = dict(
        relationships=sorted(list(relations.keys()))
    )

    if order_by is not None:
        kw['order_by'] = order_by

    if fields is not None:
        kw['fields'] = fields

    if exclude is not None:
        kw['exclude'] = exclude

    if readonly_fields is not None:
        kw['readonly_fields'] = readonly_fields

    if form_class is not None:
        kw['form_class'] = form_class

    if prepopulated_fields is not None:
        kw['prepopulated_fields'] = prepopulated_fields

    if pk_field is not None:
        kw['pk_field'] = pk_field

    if paginate_by is not None:
        kw['paginate_by'] = paginate_by

    if authenticators is not None:
        kw['authenticators'] = authenticators

    if authorisers is not None:
        kw['authorisers'] = authorisers

    mixin = modelmixin_factory(Model, **kw)

    list_view = type(
        '%sListView' % Model.__name__,
        (mixin, ListView),
        {}
    )

    detail_view = type(
        '%sDetailView' % Model.__name__,
        (mixin, DetailView),
        {}
    )

    urlpatterns.append(
        url(
            '^' + slug + '/$',
            csrf_exempt(list_view.as_view()),
            name='%s_%s_list' % (
                opts.app_label,
                opts.model_name
            )
        )
    )

    urlpatterns.append(
        url(
            (
                '^' + slug + ''
                '/(?P<' + (pk_field or 'pk') + '>[^/]+)/$'
            ),
            csrf_exempt(detail_view.as_view()),
            name='%s_%s_detail' % (
                opts.app_label,
                opts.model_name
            )
        )
    )

    for rel_name, rel_kwargs in relations.items():
        rel_fields = rel_kwargs.pop('fields', None)
        rel_exclude = rel_kwargs.pop('exclude', None)
        rel_pk_field = rel_kwargs.pop('pk_field', None)
        rel_paginate_by = rel_kwargs.pop('paginate_by', None)

        for key in rel_kwargs.keys():  # pragma: no cover
            raise TypeError(
                'relation got an unexpected property \'%s\'' % key
            )

        rel_field = opts.get_field(rel_name)
        if rel_field is None:  # pragma: no cover
            raise ConfigurationError(
                '\'%s\' field not present in %s model' % (
                    key,
                    opts.model_name
                )
            )

        rel_slug = rel_field.name
        rel_kw = {}
        rels_kw = {}

        if rel_fields is not None:
            rel_kw['fields'] = rel_fields

        if rel_exclude is not None:
            rel_kw['exclude'] = rel_exclude

        if rel_paginate_by is not None:
            rel_kw['paginate_by'] = rel_paginate_by

        if rel_pk_field is not None:
            rel_kw['pk_field'] = rel_pk_field
            rels_kw['pk_field'] = rel_pk_field

        relation_mixin = relationmixin_factory(
            Model,
            rel_field.name,
            **rel_kw
        )

        relationship_mixin = relationshipmixin_factory(
            Model,
            rel_field.name,
            **rels_kw
        )

        relation_view = type(
            '%s%sRelationView' % (
                (
                    Model.__name__,
                    rel_slug.replace('_', ' ').title().replace(' ', '')
                )
            ),
            (relation_mixin, RelationView),
            {}
        )

        relationship_view = type(
            '%s%sRelationshipView' % (
                (
                    Model.__name__,
                    rel_slug.replace('_', ' ').title().replace(' ', '')
                )
            ),
            (relationship_mixin, RelationshipView),
            {}
        )

        urlpatterns.append(
            url(
                (
                    '^' + slug + '/'
                    '(?P<' + (pk_field or 'pk') + '>[^/]+)/'
                    'relationships/' + rel_slug + '/$'
                ),
                csrf_exempt(relationship_view.as_view()),
                name='%s_%s_%s_relationship' % (
                    opts.app_label,
                    opts.model_name,
                    rel_slug
                )
            )
        )

        urlpatterns.append(
            url(
                (
                    '^' + slug + '/'
                    '(?P<' + (pk_field or 'pk') + '>[^/]+)'
                    '/' + rel_slug + '/$'
                ),
                csrf_exempt(relation_view.as_view()),
                name='%s_%s_%s' % (
                    opts.app_label,
                    opts.model_name,
                    rel_slug
                )
            )
        )

    return urlpatterns

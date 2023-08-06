from ..exceptions import AlreadyRegisteredError


class ModelResourceRegistry(object):
    def __init__(self):
        self._details = {}
        self._lists = {}

    def register(self, model, list_class=None, detail_class=None, **kwargs):
        if list_class is not None and detail_class is not None:
            return (
                self._register_list(model, list_class),
                self._register_detail(model, detail_class)
            )
        elif list_class is not None or detail_class is not None:
            raise TypeError(  # pragma: no cover
                'register takes 1 or 3 positional arguments'
            )
        else:
            from .models import ModelResource, ModelResourceList

            attrs = {
                'model': model
            }

            if 'order_by' in kwargs:
                attrs['order_by'] = kwargs['order_by']

            if 'fields' in kwargs:
                attrs['fields'] = kwargs['fields']

            if 'exclude' in kwargs:
                attrs['exclude'] = kwargs['exclude']

            if 'readonly_fields' in kwargs:
                attrs['readonly_fields'] = kwargs['readonly_fields']

            if 'form_class' in kwargs:
                attrs['form_class'] = kwargs['form_class']

            if 'pk_field' in kwargs:
                attrs['pk_field'] = kwargs['pk_field']

            detail_class = type(
                '%sResource' % model.__name__,
                (ModelResource,),
                attrs
            )

            if 'paginate_by' in kwargs:
                attrs['paginate_by'] = kwargs['paginate_by']

            list_class = type(
                '%sResourceList' % model.__name__,
                (ModelResourceList,),
                attrs
            )

            return self.register(model, list_class, detail_class)

    def _register_detail(self, model, kls):
        if model in self._details:
            raise AlreadyRegisteredError(
                '%s.%s is already registered.' % (
                    model.app_label,
                    model.model_name
                )
            )

        self._details[model] = kls
        return kls

    def _register_list(self, model, kls):
        if model in self._lists:
            raise AlreadyRegisteredError(
                '%s.%s is already registered.' % (
                    model.app_label,
                    model.model_name
                )
            )

        self._lists[model] = kls
        return kls

    def get(self, model, context):
        if context == 'list':
            return self._lists[model]

        if context == 'detail':
            return self._details[model]

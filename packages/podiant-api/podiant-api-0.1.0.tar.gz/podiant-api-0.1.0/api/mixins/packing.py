from ..exceptions import ConfigurationError


class PackingMixin(object):
    def pack(self, obj, depth=0):
        if isinstance(obj, (list, tuple, dict, bool, str, int, float)):
            return obj

        raise ConfigurationError(  # pragma: no cover
            'Unable to pack type \'%s\'' % type(obj).__name__
        )

    def get_form_class(self):
        if hasattr(self, 'form_class'):
            return self.form_class

        raise ConfigurationError(  # pragma: no cover
            'form_class not defined'
        )

    def get_initial(self):
        return {}

    def get_form_kwargs(self, form_class):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        kw = self.get_form_kwargs(form_class)
        kw.update(kwargs)
        return form_class(**kw)

from ..exceptions import ConfigurationError


class PackingMixin(object):
    def pack(self, obj, depth=0):
        if isinstance(obj, (list, tuple, dict, bool, str, int, float)):
            return obj

        raise ConfigurationError(  # pragma: no cover
            'Unable to pack type \'%s\'' % type(obj).__name__
        )

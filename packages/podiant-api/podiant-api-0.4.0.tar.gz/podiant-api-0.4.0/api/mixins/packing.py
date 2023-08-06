from ..exceptions import ConfigurationError


class PackingMixin(object):
    def pack(self, obj, depth=0):  # pragma: no cover
        if isinstance(obj, (list, tuple, dict, bool, str, int, float)):
            return obj

        raise ConfigurationError(
            'Unable to pack type \'%s\'' % type(obj).__name__
        )

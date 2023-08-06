from api.exceptions import ConfigurationError


class PackingMixin(object):
    """
    Abstract view mixing for providing a method of "packing" (turning an
    object into a JSON-serialisable list or dictionary) a given type. The
    base `pack` method only packs primitive types.
    """

    def pack(self, obj, depth=0):  # pragma: no cover
        """
        This method packs primitive types and raises a
        :class:`~exceptions.ConfigurationError` exception if a type cannot
        be packed. Override this method to pack more complex objects.
        """

        if isinstance(obj, (list, tuple, dict, bool, str, int, float)):
            return obj

        raise ConfigurationError(
            'Unable to pack type \'%s\'' % type(obj).__name__
        )

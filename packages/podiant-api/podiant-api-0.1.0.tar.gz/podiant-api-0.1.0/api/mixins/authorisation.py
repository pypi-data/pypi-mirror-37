from importlib import import_module
from .. import settings


class AuthorisationMixin(object):
    def get_authorisers(self):
        if not hasattr(self, '_authoriser_cache'):
            if hasattr(self, 'authorisers'):
                self._authoriser_cache = [
                    a(self) for a in self.authorisers
                ]
            else:
                auths = []
                for auth in settings.DEFAULT_AUTHORISERS:
                    module, klass = auth.rsplit('.', 1)
                    module = import_module(module)
                    klass = getattr(module, klass)
                    auths.append(
                        klass(self)
                    )

                self._authoriser_cache = auths

        return self._authoriser_cache

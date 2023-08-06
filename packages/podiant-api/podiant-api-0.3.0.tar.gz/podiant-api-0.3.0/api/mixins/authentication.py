from importlib import import_module
from .. import utils


class AuthenticationMixin(object):
    def get_authenticators(self):
        if not hasattr(self, '_authenticator_cache'):
            if hasattr(self, 'authenticators'):
                self._authenticator_cache = [
                    a() for a in self.authenticators
                ]
            else:
                auths = []
                for auth in utils.get_authenticators():
                    module, klass = auth.rsplit('.', 1)
                    module = import_module(module)
                    klass = getattr(module, klass)
                    auths.append(
                        klass()
                    )

                self._authenticator_cache = auths

        return self._authenticator_cache

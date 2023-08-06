from django.contrib.auth import authenticate, login
from base64 import b64decode


class AuthenticatorBase(object):
    def authenticate(self, request):  # pragma: no cover
        raise NotImplementedError('Method not implemented')


class DjangoSessionAuthenticator(AuthenticatorBase):
    def authenticate(self, request):
        if request.method in ('PATCH', 'POST', 'PUT', 'DELETE'):
            if getattr(request, '_dont_enforce_csrf_checks', False):
                return True

        a = request.user.is_authenticated
        return a if not callable(a) else a()


class HTTPBasicAuthenticator(AuthenticatorBase):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')

        if auth.startswith('Basic '):
            try:
                auth = b64decode(auth[6:]).decode('utf-8')
            except Exception:  # pragma: no cover
                return False

            try:
                username, password = auth.split(':', 1)
            except Exception:  # pragma: no cover
                return False

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return True

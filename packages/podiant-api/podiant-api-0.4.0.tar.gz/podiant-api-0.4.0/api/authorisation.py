from .exceptions import (
    ConfigurationError,
    ForbiddenError,
    NotAuthenticatedError
)


class AuthBundle(object):
    context = ''
    data = {}

    def __init__(self, context='', **kwargs):
        self.context = context
        self.data.update(kwargs)


class AuthoriserBase(object):
    def __init__(self, view):
        self.view = view

    def has_list_permission(self, request, bundle):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_detail_permission(self, request, bundle):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_create_permission(self, request, bundle):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_update_permission(self, request, bundle):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_delete_permission(self, request, bundle):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def authorise(self, request, bundle):
        perm, perm_name = None, None

        if bundle.context == 'list':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_list_permission
                perm_name = 'list'
            elif request.method == 'POST':
                perm = self.has_create_permission
                perm_name = 'create'
        elif bundle.context == 'detail':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_detail_permission
                perm_name = 'detail'
            elif request.method in ('PUT', 'PATCH'):
                perm = self.has_update_permission
                perm_name = 'update'
            elif request.method == 'DELETE':
                perm = self.has_delete_permission
                perm_name = 'delete'

        if perm is None or not perm(request, bundle):
            raise ForbiddenError(
                'Operation not permitted.',
                {
                    'permission': perm_name
                }
            )


class ReadOnlyAuthoriser(AuthoriserBase):
    def has_list_permission(self, request, bundle):
        return True

    def has_detail_permission(self, request, bundle):
        return True

    def has_create_permission(self, request, bundle):
        return False

    def has_update_permission(self, request, bundle):
        return False

    def has_delete_permission(self, request, bundle):
        return False


class DjangoUserAuthoriser(AuthoriserBase):
    def is_anonymous(self, request):
        a = request.user.is_anonymous
        return a if not callable(a) else a()

    def has_model_perm(self, request, perm, obj=None):
        if not hasattr(self.view, 'model'):  # pragma: no cover
            raise ConfigurationError('Model not defined')

        if self.is_anonymous(request):
            raise NotAuthenticatedError(
                'User not authenticated, or authentication details invalid.'
            )

        if perm == 'view':
            return True

        perm = '%s.%s_%s' % (
            self.view.model._meta.app_label,
            perm,
            self.view.model._meta.model_name
        )

        return request.user.has_perm(perm)

    def has_list_permission(self, request, bundle):
        return self.has_model_perm(
            request,
            'view',
            bundle.data.get('object')
        )

    def has_detail_permission(self, request, bundle):
        return self.has_model_perm(
            request,
            'view',
            bundle.data.get('object')
        )

    def has_create_permission(self, request, bundle):
        return self.has_model_perm(
            request,
            'add',
            bundle.data.get('object')
        )

    def has_update_permission(self, request, bundle):
        return self.has_model_perm(
            request,
            'change',
            bundle.data.get('object')
        )

    def has_delete_permission(self, request, bundle):
        return self.has_model_perm(
            request,
            'delete',
            bundle.data.get('object')
        )


class GuestReadOnlyOrDjangoUserAuthoriser(DjangoUserAuthoriser):
    def has_list_permission(self, request, bundle):
        if self.is_anonymous(request):
            return True

        return super().has_list_permission(request, bundle)

    def has_detail_permission(self, request, bundle):
        if self.is_anonymous(request):
            return True

        return super().has_detail_permission(request, bundle)

    def authorise(self, request, bundle):
        if bundle.context == 'list':
            super().authorise(request, bundle)
            return

        perm, perm_name = None, None
        if request.method in ('GET', 'HEAD'):
            perm = self.has_detail_permission
            perm_name = 'detail'
        elif request.method in ('PUT', 'PATCH'):
            perm = self.has_update_permission
            perm_name = 'update'
        elif request.method == 'DELETE':
            perm = self.has_delete_permission
            perm_name = 'delete'

        if perm is None or not perm(request, bundle):
            raise ForbiddenError(
                'Operation not permitted.',
                {
                    'permission': perm_name
                }
            )

from .exceptions import (
    ConfigurationError,
    ForbiddenError,
    NotAuthenticatedError
)


class AuthoriserBase(object):
    def __init__(self, view):
        self.view = view

    def has_list_permission(self, request):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_detail_permission(self, request, obj=None):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_create_permission(self, request):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_update_permission(self, request, obj=None):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def authorise(self, request, context):
        perm, perm_name = None, None

        if context == 'list':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_list_permission
                perm_name = 'list'
            elif request.method == 'POST':
                perm = self.has_create_permission
                perm_name = 'create'
        elif context == 'detail':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_detail_permission
                perm_name = 'detail'
            elif request.method in ('PUT', 'PATCH'):
                perm = self.has_update_permission
                perm_name = 'update'
            elif request.method == 'DELETE':
                perm = self.has_delete_permission
                perm_name = 'delete'

        if perm is None or not perm(request):
            raise ForbiddenError(
                'Operation not permitted.',
                {
                    'permission': perm_name
                }
            )


class ReadOnlyAuthoriser(AuthoriserBase):
    def has_list_permission(self, request):
        return True

    def has_detail_permission(self, request, obj=None):
        return True

    def has_create_permission(self, request):
        return False

    def has_update_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
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

    def has_list_permission(self, request):
        return self.has_model_perm(request, 'view')

    def has_detail_permission(self, request, obj=None):
        return self.has_model_perm(request, 'view', obj)

    def has_create_permission(self, request):
        return self.has_model_perm(request, 'add')

    def has_update_permission(self, request, obj=None):
        return self.has_model_perm(request, 'change', obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_model_perm(request, 'delete', obj)


class GuestReadOnlyOrDjangoUserAuthoriser(DjangoUserAuthoriser):
    def has_list_permission(self, request):
        if self.is_anonymous(request):
            return True

        return super().has_list_permission(request)

    def has_detail_permission(self, request, obj=None):
        if self.is_anonymous(request):
            return True

        return super().has_detail_permission(request, obj)

    def authorise(self, request, context):
        if context == 'list':
            super().authorise(request, context)
            return

        perm, perm_name = None, None
        obj = self.view.get_object()

        if request.method in ('GET', 'HEAD'):
            perm = self.has_detail_permission
            perm_name = 'detail'
        elif request.method in ('PUT', 'PATCH'):
            perm = self.has_update_permission
            perm_name = 'update'
        elif request.method == 'DELETE':
            perm = self.has_delete_permission
            perm_name = 'delete'

        if perm is None or not perm(request, obj):
            raise ForbiddenError(
                'Operation not permitted.',
                {
                    'permission': perm_name
                }
            )

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

    def has_detail_permission(self, request, obj):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_create_permission(self, request):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_update_permission(self, request, obj):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        raise NotImplementedError('Methot not implemented')

    def authorise(self, request, context):
        perm = None

        if context == 'list':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_list_permission
            elif request.method == 'POST':
                perm = self.has_create_permission
        elif context == 'detail':
            if request.method in ('GET', 'HEAD'):
                perm = self.has_detail_permission
            elif request.method in ('PUT', 'PATCH'):
                perm = self.has_update_permission
            elif request.method == 'DELETE':
                perm = self.has_delete_permission

        if perm is None or not perm(request):
            raise ForbiddenError('Operation not permitted.')


class ReadOnlyAuthoriser(AuthoriserBase):
    def has_list_permission(self, request):
        return True

    def has_detail_permission(self, request, obj):
        return True

    def has_create_permission(self, request):
        return False

    def has_update_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DjangoUserAuthoriser(AuthoriserBase):
    def is_anonymous(self, request):
        a = request.user.is_anonymous
        return callable(a) and a() or a

    def has_model_perm(self, request, perm, obj=None):
        if not hasattr(self.view, 'model'):  # pragma: no cover
            raise ConfigurationError('Model not defined')

        if self.is_anonymous(request):
            raise NotAuthenticatedError(
                'User not authenticated, or authentication details invalid.'
            )

        perm = '%s.%s_%s' % (
            self.view.model._meta.app_label,
            perm,
            self.view.model._meta.model_name
        )

        return request.user.has_perm(perm, obj)

    def has_list_permission(self, request):
        return self.has_model_perm(request, 'view')

    def has_detail_permission(self, request, obj):
        return self.has_model_perm(request, 'view', obj)

    def has_create_permission(self, request):
        return self.has_model_perm(request, 'add')

    def has_update_permission(self, request, obj):
        return self.has_model_perm(request, 'change', obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_model_perm(request, 'delete', obj)


class GuestReadOnlyOrDjangoUserAuthoriser(DjangoUserAuthoriser):
    def has_list_permission(self, request):
        if self.is_anonymous(request):
            return True

        return super().has_list_permission(request)

    def has_detail_permission(self, request, obj):
        if self.is_anonymous(request):
            return True

        return super().has_detail_permission(request, obj)

    def authorise(self, request, context):
        if context == 'list':
            super().authorise(request, context)
            return

        perm = None
        if context == 'detail':
            obj = self.view.get_object()
            if request.method in ('GET', 'HEAD'):
                perm = self.has_detail_permission
            elif request.method in ('PUT', 'PATCH'):
                perm = self.has_update_permission
            elif request.method == 'DELETE':
                perm = self.has_delete_permission

        if perm is None or not perm(request, obj):
            raise ForbiddenError('Operation not permitted.')

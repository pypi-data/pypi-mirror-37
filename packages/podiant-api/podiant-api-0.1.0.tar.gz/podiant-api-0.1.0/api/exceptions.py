class ConfigurationError(Exception):
    pass


class MethodNotAllowedError(Exception):
    pass


class BadRequestError(Exception):
    pass


class UnprocessableEntityError(BadRequestError):
    pass


class NotAuthenticatedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class ConflictError(Exception):
    pass

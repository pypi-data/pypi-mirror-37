from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from .exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    MethodNotAllowedError,
    NotAuthenticatedError,
    UnprocessableEntityError
)

from . import settings
import json
import logging


def handle_exceptions():
    def wrapper(f):
        def a(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except NotAuthenticatedError as ex:
                e = {
                    'status': 401,
                    'title': 'Unauthorized'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=401,
                    content_type='application/json'
                )
            except UnprocessableEntityError as ex:
                e = {
                    'status': 422,
                    'title': 'Unprocessable Entity'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                    if len(ex.args) > 1:
                        e['meta'] = ex.args[1]

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=422,
                    content_type='application/json'
                )
            except BadRequestError as ex:
                e = {
                    'status': 400,
                    'title': 'Bad Request'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=400,
                    content_type='application/json'
                )
            except ForbiddenError as ex:
                e = {
                    'status': 403,
                    'title': 'Forbidden'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                    if len(ex.args) > 1:
                        e['meta'] = ex.args[1]

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=403,
                    content_type='application/json'
                )
            except (ObjectDoesNotExist, Http404) as ex:
                e = {
                    'status': 404,
                    'title': 'Not Found'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=404,
                    content_type='application/json'
                )
            except MethodNotAllowedError as ex:
                e = {
                    'status': 405,
                    'title': 'Method Not Allowed'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=405,
                    content_type='application/json'
                )
            except ConflictError as ex:
                e = {
                    'status': 409,
                    'title': 'Conflict'
                }

                if any(ex.args):
                    e['detail'] = str(ex.args[0])

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=409,
                    content_type='application/json'
                )
            except Exception as ex:
                e = {
                    'status': 500,
                    'title': 'Internal Server Error'
                }

                if settings.DEBUG:
                    if any(ex.args):
                        e['detail'] = str(ex.args[0])

                    if len(ex.args) > 1:
                        e['meta'] = ex.args[1]

                logger = logging.getLogger('podiant.api')
                logger.error('Error processing API request', exc_info=True)

                return HttpResponse(
                    json.dumps(
                        {
                            'error': e
                        },
                        indent=2
                    ),
                    status=500,
                    content_type='application/json'
                )

        return a

    return wrapper

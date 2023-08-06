from logging import getLogger
from django.http.response import HttpResponse
from ..exceptions import BadRequestError
import json


class JSONMixin(object):
    def deserialise(self, data):
        logger = getLogger('podiant.api')

        try:
            return json.loads(data.decode('utf-8'))
        except json.decoder.JSONDecodeError as ex:
            logger.debug('Error parsing JSON request', exc_info=True)
            raise BadRequestError(str(ex.args[0]))

    def serialise(self, content):
        return json.dumps(
            content,
            indent=2
        )

    def respond(self, content, *args, **kwargs):
        return HttpResponse(
            content=self.serialise(content),
            content_type='application/vnd.api+json',
            *args,
            **kwargs
        )

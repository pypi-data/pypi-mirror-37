from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models import FieldDoesNotExist
from .exceptions import UnprocessableEntityError
from .utils import get_id_field, unurlise_field_name


def qs_name_to_kwarg(name, context):
    parts = unurlise_field_name(name).split('.')
    found_parts = []

    while True:
        part = parts.pop(0)

        try:
            field = context.get_field(part)
        except FieldDoesNotExist:
            raise UnprocessableEntityError(
                'Invalid filter field',
                {
                    'field': name
                }
            )

        if isinstance(field, (ForeignKey, ManyToManyField)):
            if not any(parts):
                found_parts.append(part)
                found_parts.append(
                    get_id_field(
                        field.related_model
                    )
                )
            else:
                context = field.related_model._meta
                found_parts.append(part)
        elif any(parts):
            raise UnprocessableEntityError(
                'Invalid filter field',
                {
                    'field': name
                }
            )
        else:
            found_parts.append(part)

        if not any(parts):
            break

    return '__'.join(found_parts)

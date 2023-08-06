from api.resources import registry
from api.utils import get_id_field
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from .packing import PackingMixin


class ModelMixin(PackingMixin):
    """
    View mixin for packing and unpacking Django model instances.
    """

    def get_resource_kwargs(self):  # pragma: no cover
        """
        This method returns a dictionary of kwargs to be passed when
        instantiating a resource or resource list.
        """

        return {}

    def get_resource(self):
        """
        Helper method to return the resource for this view. Requires the
        setting of a `resource_class` property.
        """

        if not hasattr(self, '_resource_cache'):
            if hasattr(self, 'resource_class'):
                self._resource_cache = self.resource_class(
                    **self.get_resource_kwargs()
                )
            else:
                self._resource_cache = registry.get(
                    self.model, 'detail'
                )(
                    **self.get_resource_kwargs()
                )

        return self._resource_cache

    def patch_form_fields(self, form):
        """
        Overrides model-choice form fields so that resources that don't use a
        standard primary key can allow related forms to specify the object
        with the non-standard key.
        """

        for name, field in form.fields.items():
            if isinstance(field, (ModelChoiceField, ModelMultipleChoiceField)):
                field.to_field_name = get_id_field(field.queryset.model)

from .base import ResourceDetailBase, ResourceListBase
from .models import ModelResource, ModelResourceList
from .manager import ModelResourceRegistry
from .links import ResourceLink


registry = ModelResourceRegistry()


__all__ = [
    'ResourceDetailBase',
    'ResourceListBase',
    'ModelResource',
    'ModelResourceList',
    'ResourceLink',
    'registry'
]

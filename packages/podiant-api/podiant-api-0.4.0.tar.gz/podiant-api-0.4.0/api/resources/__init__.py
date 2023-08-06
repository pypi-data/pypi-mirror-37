from .base import ResourceBase
from .models import ModelResource
from .manager import ModelResourceRegistry


registry = ModelResourceRegistry()


__all__ = [
    'ResourceBase',
    'ModelResource',
    'registry'
]

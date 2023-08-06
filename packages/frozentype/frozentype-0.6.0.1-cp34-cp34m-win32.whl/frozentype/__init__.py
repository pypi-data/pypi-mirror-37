from .frozendict import FrozenDict
from .frozenmap import FrozenMap
from ._frozendict import frozendict

from collections import Mapping
Mapping.register(frozendict)

__all__ = ['frozendict', 'FrozenDict', 'FrozenDict']
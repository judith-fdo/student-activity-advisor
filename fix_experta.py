"""
Compatibility patch for experta with Python 3.10+
Fixes the collections.Mapping AttributeError
"""

import sys
import collections
import collections.abc

# Fix for Python 3.10+ where collections.Mapping was moved to collections.abc
for type_name in ['Mapping', 'MutableMapping', 'Iterable', 'MutableSet', 'Callable']:
    if not hasattr(collections, type_name):
        setattr(collections, type_name, getattr(collections.abc, type_name))

print("✓ Experta compatibility patch applied")
#cython: language_level=3
#cython: embedsignature=True

from collections import Mapping

class FrozenDict:
    """FrozenDict: an immutable mapping object wrapped around a dict object"""

    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
        self._hash = 0
    #
    def __iter__(self):
        return iter(self._data)
    #
    def __len__(self):
        return len(self._data)
    #
    def __getitem__(self, key):
        return self._data[key]
    #
    def __contains__(self, key):
        return key in self._data
    
    def __iter__(self):
        for key in self._data:
            yield key
    #
    def __hash__(self):
        if self._hash == 0:
            x = 0
            for pair in self._data.items():
                x ^= hash(pair)
            self._hash = x
        return self._hash
    
    def get(self, key, value=None):
        return self._data.get(key, value)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
    
    def copy(self):
        return FrozenDict(self._data)
    
    def __reduce__(self):
        return FrozenDict, (self._data,)
    
    def __nonzero__(self):
        return bool(self._data)

    def __eq__(self, other):
        return self._data == other
    
    def __repr__(self):
        if self._data:
            return "FrozenDict(" + repr(self._data) + ")"
        else:
            return "FrozenDict()"

    def __str__(self):
        if self._data:
            return "FrozenDict(" + str(self._data) + ")"
        else:
            return "FrozenDict()"

Mapping.register(FrozenDict)

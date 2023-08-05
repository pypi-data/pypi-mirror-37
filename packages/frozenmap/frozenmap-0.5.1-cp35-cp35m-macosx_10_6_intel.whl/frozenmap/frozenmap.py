#cython: language_level=3
#cython: embedsignature=True

from collections import Mapping        

class FrozenMap:
    """FrozenMap: an immutable mapping object wrapped around a mutable mapping object"""

    def __init__(self, ob):
        self._data = ob
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
        for key in self._data.keys():
            yield key
    #
    def __hash__(self):
        if self._hash == 0:
            x = 0
            _data = self._data
            for key in _data.keys():
                y = hash( (key, _data[key]) )
                x ^= y
            self._hash = x
        return self._hash
    
    def get(self, key, value=None):
        return self._data.get(key, value)

    def keys(self):
        _data = self._data
        for key in _data.keys():
            yield key

    def values(self):
        _data = self._data
        for key in _data.keys():
            yield _data[key]

    def items(self):
        _data = self._data
        for key in _data.keys():
            yield (key, _data[key])
    
    def copy(self):
        return FrozenMap(self._data)
    
    def __reduce__(self):
        return FrozenMap, (self._data,)
    
    def __nonzero__(self):
        return bool(self._data)

    def __eq__(self, other):
        return self._data == other
    
    def __str__(self):
        if self._data:
            return "FrozenMap(" + str(self._data) + ")"
        else:
            return "FrozenMap()"

Mapping.register(FrozenMap)

#cython: language_level=3
#cython: embedsignature=True

import cython

from collections import Mapping
from sys import maxsize, getsizeof

class FrozenMap:
    """FrozenMap: an immutable mapping object wrapped around a mutable mapping object"""

    def __init__(self, ob):
        self._data = ob
        self._hash = -1
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
        if self._hash == -1:
            x = 0
            _data = self._data
            for key in _data.keys():
                y = hash( (key, _data[key]) )
                x ^= y
            x ^= maxsize
            if x == -1:
                x = -2
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

    def __richcmp__(self, other, flag):
        try:
            if flag == 2:
                return self._data == other
            elif flag == 3:
                return self._data != other
        except TypeError:
            pass

        mro = other.__class__.__mro__
        if Mapping not in mro:
            return NotImplemented

        switch = True
        if flag == 0:    # LESS THAN
            if len(self) >= len(other):
                return False
            little, big = self, other

        elif flag == 1:  # LESS THAN OR EQUAL
            if len(self) > len(other):
                return False
            little, big = self, other

        elif flag == 2:    # EQUAL
            if len(self) != len(other):
                return False
            little, big = self, other

        elif flag == 3:  # NOT EQUAL
            if len(self) != len(other):
                return True
            little, big = self, other
            switch = False

        elif flag == 4:  # GREATER THAN
            if len(self) <= len(other):
                return False
            little, big = other, self

        elif flag == 5:  # GREATER THAN OR EQUAL
            if len(self) < len(other):
                return False
            little, big = other, self

        try:
            for k in little:
                if little[k] != big[k]:
                    return not switch
            return switch
        except KeyError:
            return not switch
        
    
    def __str__(self):
        if self._data:
            return "FrozenMap(" + str(self._data) + ")"
        else:
            return "FrozenMap()"
    
    def __sizeof__(self):
        return getsizeof(self._data) + cython.sizeof(self._hash)

Mapping.register(FrozenMap)

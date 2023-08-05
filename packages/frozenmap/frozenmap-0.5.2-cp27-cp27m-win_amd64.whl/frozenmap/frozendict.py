#cython: language_level=3
#cython: embedsignature=True

import cython

from collections import Mapping
from sys import maxsize, getsizeof

class FrozenDict:
    """FrozenDict: an immutable mapping object wrapped around a dict object"""

    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
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
        for key in self._data:
            yield key
    #
    def __hash__(self):
        if self._hash == -1:
            x = 0
            for pair in self._data.items():
                x ^= hash(pair)
            x ^= maxsize
            if x == -1:
                x = -2
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
    
    @classmethod
    def fromkeys(cls, keys, value):
        return FrozenDict(((key, value) for key in keys))    
    
    def __reduce__(self):
        return FrozenDict, (self._data,)
    
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
        if flag == 0:    # <
            if len(self) >= len(other):
                return False
            little, big = self, other

        elif flag == 1:  # <=
            if len(self) > len(other):
                return False
            little, big = self, other

        elif flag == 2:    # ==
            if len(self) != len(other):
                return False
            little, big = self, other

        elif flag == 3:  # !=
            if len(self) != len(other):
                return True
            little, big = self, other
            switch = False

        elif flag == 4:  # >
            if len(self) <= len(other):
                return False
            little, big = other, self

        elif flag == 5:  # >=
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
        
    def __sizeof__(self):
        return getsizeof(self._data) + cython.sizeof(self._hash)
        

Mapping.register(FrozenDict)

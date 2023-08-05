=========
frozenmap
=========

**frozenmap** is `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library.
It implements ``FrozenDict`` and ``FrozenMap`` classes. 

* `FrozenMap` instance is an immutable mapping object wrapped around a mutable mapping object.
* `FrozenDict` instance is an immutable mapping object wrapped around a dict object.

This library actually is a "proof of concept" for the problem of fast "immutable dict" problem.

Main repository for ``frozenmap`` 
is on `bitbucket <https://bitbucket.org/intellimath/frozenmap>`_.

Quick start:
------------

First load inventory::

    >>> from frozenmap import FrozenDict

Simple example::

    >>> fd = FrozenDict(a=1,b=2,c=3)
    >>> print(fp)
    FrozenDict({'a':1, 'b':2, 'c':3})
    >>> fd['a']
    1
    >>> fd['a'] = 10
    ........
    TypeError: 'frozenmap.frozendict.FrozenDict' object does not support item assignment
    >>> del fd['a']
    .........
    TypeError: 'frozenmap.frozendict.FrozenDict' object does not support item deletion
    >>> fd.pop('a')
    .........
    AttributeError: 'frozenmap.frozendict.FrozenDict' object has no attribute 'pop'
   

Changes:
--------

**0.5** Initial version


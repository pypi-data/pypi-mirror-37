==========
frozentype
==========

**frozentype** is `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library.
It implements some frozen python types: ``frozendict`` type (in C) and ``FrozenDict``, ``FrozenMap`` classes (in Cython). 

* `frozendict` is read-only and hashable dictionary (C based).
* `FrozenMap` is read-only mapping object wrapped around a mutable mapping object (Cython based).
* `FrozenDict` is read-only and hashable dictionary (Cython based).

This library actually is an attempt to proof the concept of fast frozendict (C/Cython based).

Main repository for ``frozentype`` 
is on `bitbucket <https://bitbucket.org/intellimath/frozentype>`_.

Quick start:
------------


First load inventory::

    >>> from frozentype import frozendict, FrozenDict

Simple example::

    >>> fd = frozendict(a=1,b=2,c=3)
    >>> fd
    frozendict({'a': 1, 'b': 2, 'c': 3})
    >>> fd['a']
    1
    >>> fd['a'] = 10
    ........
    TypeError: 'frozentype._frozendict.frozendict' object does not support item assignment
    >>> del fd['a']
    .........
    TypeError: 'frozentype._frozendict.frozendict' object does not support item deletion
    >>> fd.pop('a')
    .........
    AttributeError: 'frozentype._frozendict.frozendict' object has no attribute 'pop'
 

    >>> fd = FrozenDict(a=1,b=2,c=3)
    >>> print(fp)
    FrozenDict({'a': 1, 'b': 2, 'c': 3})
    >>> fd['a']
    1
    >>> fd['a'] = 10
    ........
    TypeError: 'frozentype.frozendict.FrozenDict' object does not support item assignment
    >>> del fd['a']
    .........
    TypeError: 'frozentype.frozendict.FrozenDict' object does not support item deletion
    >>> fd.pop('a')
    .........
    AttributeError: 'frozentype.frozendict.FrozenDict' object has no attribute 'pop'
   

Changes:
--------

** 0.6.0.1 ** (technical version to convince pypi to upload project with fixed title in README)

** 0.6 ** (migrate from project intellimath/frozenmap)

* Add C implementation for `frozendict`.
* Add tests for frozendict type.

**0.5** Initial version


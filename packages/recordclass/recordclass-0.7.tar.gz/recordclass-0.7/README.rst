===========
recordclass
===========

**recordclass** is `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library.
It implements the type ``memoryslots`` and factory function ``recordclass`` 
in order to create record-like classes. 

* ``memoryslots`` is ``tuple``-like type, which supports assignment operations. 
* ``recordclass`` is a factory function that create a "mutable" analog of 
  ``collection.namedtuple``.

This library actually is a "proof of concept" for the problem of fast "mutable" 
alternative of ``namedtuple``.

Main repository for ``recordclass`` 
is on `bitbucket <https://bitbucket.org/intellimath/recordclass>`_.

Here is also a simple `example <http://nbviewer.ipython.org/urls/bitbucket.org/intellimath/recordclass/raw/default/examples/what_is_recordclass.ipynb>`_.

Quick start:
------------

First load inventory::

    >>> from recordclass import recordclass, RecordClass

Simple example with ``recordclass``::

    >>> Point = recordclass('Point', 'x y')
    >>> p = Point(1,2)
    >>> print(p)
    Point(1, 2)
    >>> print(p.x, p.y)
    1 2
    >>> p.x, p.y = 10, 20
    >>> print(p.x, p.y)
    10 20
    
Simple example with ``RecordClass`` and typehints::

    class Point(RecordClass):
       x: int
       y: int
       
    >>> p = Point(1, 2)
    >>> print(p)
    Point(1, 2)
    >>> print(p.x, p.y)
    1 2
    >>> p.x, p.y = 10, 20
    >>> print(p.x, p.y)
    10 20


Changes:
--------

**0.7**

* Make memoryslots objects creation faster. As a side effect: when number of fields >= 8
  recordclass instance creation time is not biger than creation time of instaces of
  dataclasses with __slots__.
* Recordclass factory function now create new recordclass classes in the same way as namedtuple in 3.7 
  (there is no compilation of generated python source of class).

**0.6**

* Add support for default values in recordclass factory function in correspondence
  to same addition to namedtuple in python 3.7.

**0.5**

* Change version to 0.5

**0.4.4**

* Add support for default values in RecordClass (patches from Pedro von Hertwig)
* Add tests for RecorClass (adopted from python tests for NamedTuple)

**0.4.3**

* Add support for typing for python 3.6 (patches from Vladimir Bolshakov).
* Resolve memory leak issue.

**0.4.2**

* Fix memory leak in property getter/setter



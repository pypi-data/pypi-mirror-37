from keyword import iskeyword as _iskeyword
import re

from .memoryslots import memoryslots

def isidentifier(s):
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None

import sys as _sys
_PY3 = _sys.version_info[0] >= 3

if _PY3:
    _intern = _sys.intern
else:
    from __builtin__ import intern as _intern

_class_template = """\
from collections import OrderedDict
from recordclass.memoryslots import memoryslots, itemgetset

_property = property
_tuple = tuple
_memoryslots = memoryslots
_memoryslots_new = memoryslots.__new__
_itemgetset = itemgetset

class {typename}(memoryslots):
    '{typename}({arg_list})'

    __slots__ = ()

    _fields = {field_names!r}
    _fields_defaults = {field_defaults!r}
     

    def __new__(_cls, {arg_list}):
        'Create new instance of {typename}({arg_list})'
        return _memoryslots_new(_cls, {arg_list})

    @classmethod
    def _make(_cls, iterable):
        'Make a new {typename} object from a sequence or iterable'
        result = _memoryslots_new(_cls, *iterable)
        if len(result) != {num_fields:d}:
            raise TypeError('Expected {num_fields:d} arguments, got %d' % len(result))
        return result

    def _replace(_self, **kwds):
        'Return a new {typename} object replacing specified fields with new values'
        for name, val in kwds.items():
            setattr(_self, name, val)
        return _self

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '({repr_fmt})' % tuple(self)

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values'
        return OrderedDict(zip(self.__class__._fields, self ))

    __dict__ = _property(_asdict)
        
    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        return None
        
    def __reduce__(self):
        'Reduce'
        return type(self), tuple(self)

{field_defs}
"""

_repr_template = '{name}=%r'

_field_template = '    {name} = _itemgetset({index:d})'

# _field_template = '''\
#     def __{name}_get(self):
#         return self[{index:d}]
#     def __{name}_set(self, val):
#         self[{index:d}] = val
#     {name} = _property(__{name}_get, __{name}_set, doc='Alias for field number {index:d}')
#     del __{name}_set, __{name}_get'''


def recordclass(typename, field_names, rename=False, defaults=None, module=None, verbose=False, source=True):
    """Returns a new subclass of array with named fields.

    >>> Point = recordarray('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    """

    # Validate the field names.  At the user's option, either generate an error
    # message or automatically replace the field name with a valid name.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    else:
        field_names = list(map(str, field_names))
    typename = _intern(str(typename))
    if rename:
        seen = set()
        for index, name in enumerate(field_names):
            if (not isidentifier(name)
                or _iskeyword(name)
                or name.startswith('_')
                or name in seen):
                field_names[index] = '_%d' % index
            seen.add(name)

    for name in [typename] + field_names:
        if type(name) != str:
            raise TypeError('Type names and field names must be strings')
        if not isidentifier(name):
            raise ValueError('Type names and field names must be valid '
                             'identifiers: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a '
                             'keyword: %r' % name)
    seen = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: '
                             '%r' % name)
        if name in seen:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen.add(name)

    if defaults is not None:
        defaults = tuple(defaults)
        if len(defaults) > len(field_names):
            raise TypeError('Got more default values than field names')
        field_defaults = dict(reversed(list(zip(reversed(field_names),
                                                reversed(defaults)))))
    else:
        field_defaults = {}

    field_names = tuple(map(_intern, field_names))
    num_fields = len(field_names)
    arg_list = repr(field_names).replace("'", "")[1:-1]
    repr_fmt=', '.join(_repr_template.format(name=name) for name in field_names)
    field_defs='\n'.join(_field_template.format(index=index, name=name)
                         for index, name in enumerate(field_names))
        
    # Fill-in the class template
    class_definition = _class_template.format(
        typename=typename,
        field_names=field_names,
        field_defaults=field_defaults,
        num_fields=num_fields,
        arg_list=arg_list,
        repr_fmt=repr_fmt,
        field_defs=field_defs
    )

    # Execute the template string in a temporary namespace and support
    # tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(_memoryslots_new=memoryslots.__new__, 
                     __name__='recordclass_' + typename)
    
    code = compile(class_definition, "", "exec")
    eval(code, namespace)
    result = namespace[typename]
    
    if defaults is not None:
        result.__new__.__defaults__ = defaults    
    if source:
        result._source = class_definition
    if verbose:
        print(result._source)

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython).
    if module is None:
        try:
            module = _sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass
    if module is not None:
        result.__module__ = module    

    return result

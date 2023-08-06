import collections
from recordclass.record import recordclass
from typing import _type_check

__version__ = '0.6'

import sys as _sys
_PY36 = _sys.version_info[:2] >= (3, 6)

_prohibited = ('__new__', '__init__', '__slots__', '__getnewargs__',
               '_fields', '_field_defaults', '_field_types',
               '_make', '_replace', '_asdict', '_source')

_special = ('__module__', '__name__', '__qualname__', '__annotations__')

def _make_recordclass(name, types):
    msg = "RecordClass('Name', [(f0, t0), (f1, t1), ...]); each t must be a type"
    types = [(n, _type_check(t, msg)) for n, t in types]
    rec_cls = recordclass(name, [n for n, t in types])
    rec_cls.__annotations__ = rec_cls._field_types = dict(types)
    try:
        rec_cls.__module__ = _sys._getframe(2).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    return rec_cls

class RecordClassMeta(type):
    def __new__(cls, typename, bases, ns):
        if ns.get('_root', False):
            return super().__new__(cls, typename, bases, ns)
        types = ns.get('__annotations__', {})

        defaults = []
        defaults_dict = {}
        for field_name in types:
            if field_name in ns:
                default_value = ns[field_name]
                defaults.append(default_value)
                defaults_dict[field_name] = default_value
            elif defaults:
                raise TypeError("Non-default recordclass field {field_name} cannot "
                                "follow default field(s) {default_names}"
                                .format(field_name=field_name,
                                        default_names=', '.join(defaults_dict.keys())))

        rec_cls = _make_recordclass(typename, types.items())

        rec_cls.__new__.__defaults__ = tuple(defaults)
        rec_cls.__new__.__annotations__ = collections.OrderedDict(types)
        rec_cls._field_defaults = defaults_dict
        # update from user namespace without overriding special recordclass attributes
        for key in ns:
            if key in _prohibited:
                raise AttributeError("Cannot overwrite RecordClass attribute " + key)
            elif key not in _special and key not in rec_cls._fields:
                setattr(rec_cls, key, ns[key])

        return rec_cls


class RecordClass(metaclass=RecordClassMeta):
    _root = True

    def __new__(self, typename, fields=None, **kwargs):
        if fields is None:
            fields = kwargs.items()
        elif kwargs:
            raise TypeError("Either list of fields or keywords"
                            " can be provided to RecordClass, not both")
        return _make_recordclass(typename, fields)

import collections

import logging
logger = logging.getLogger(__name__)

GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY = 'GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY'
GLUE_PLATE_PLUS_BEFORE = 'GLUE_PLATE_PLUS_BEFORE_'
GLUE_PLATE_PLUS_AFTER = 'GLUE_PLATE_PLUS_AFTER_'
GLUE_PLATE_PARENT_MODULES = 'GLUE_PLATE_PARENT_MODULES'

def _update(org, opt):
    for k, v in opt.items():
        if k.startswith(GLUE_PLATE_PLUS_BEFORE) and isinstance(v, list):
            _k = k[len(GLUE_PLATE_PLUS_BEFORE):]
            org[_k] = v + org[_k]
        elif k.startswith(GLUE_PLATE_PLUS_AFTER) and isinstance(v, list):
            _k = k[len(GLUE_PLATE_PLUS_AFTER):]
            org[_k] = org[_k] + v
        elif isinstance(v, collections.Mapping):
            r = _update(org.get(k, Glue()), v)
            org[k] = r
        else:
            org[k] = opt[k]
    return org


class Glue(dict):
    '''dict like object. accessible with dot syntax.
    >>> settings = Glue(
    ...   spam = '123',
    ...   egg = 123,
    ...   lst = [1,2,3],
    ... )
    >>> assert(settings.spam == '123')
    >>> assert(settings.egg == 123)
    >>> assert(settings.lst == [1,2,3])
    >>> settings.ham = 123.0
    >>> assert(settings.ham == 123.0)
    >>> s2 = Glue(dict(spam=456))
    >>> settings.update(s2)
    >>> assert(settings.spam == 456)
    >>> assert(settings.ham == 123.0)
    >>> s3 = Glue(GLUE_PLATE_PLUS_BEFORE_lst=[0])
    >>> settings.update(s3)
    >>> assert(settings.lst == [0,1,2,3])
    >>> s4 = Glue(GLUE_PLATE_PLUS_AFTER_lst=[4])
    >>> settings.update(s4)
    >>> assert(settings.lst == [0,1,2,3,4])
    '''

    def __init__(self, *args, **kwargs):
        for d in args:
            if isinstance(d, collections.Mapping):
                self.update(d)
        for key, value in kwargs.items():
            self[key] = value

    def __setattr__(self, key, value):
        if isinstance(value, collections.Mapping):
            self[key] = Glue(value)
        else:
            self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            object.__getattribute__(self, key)

    def update(self, opt):
        self = _update(self, opt)

from copy import deepcopy

import numpy as np
from funcy import decorator

RANDOM_STATE = 1754


def asarray2d(a):
    """Cast to 2d array"""
    arr = np.asarray(a)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    return arr


def get_arr_desc(arr):
    """Get array description, in the form '<array type> <array shape>'"""
    desc = '{typ} {shp}'
    typ = type(arr)
    shp = getattr(arr, 'shape', None)
    return desc.format(typ=typ, shp=shp)


def get_enum_keys(cls):
    return [attr for attr in dir(cls) if not attr.startswith('_')]


def get_enum_values(cls):
    return [getattr(cls, attr) for attr in get_enum_keys(cls)]


def indent(text, n=4):
    """Indent each line of text by n spaces"""
    _indent = ' ' * n
    return '\n'.join(_indent + line for line in text.split('\n'))


def make_plural_suffix(obj, suffix='s'):
    if len(obj) != 1:
        return suffix
    else:
        return ''


@decorator
def whether_failures(call):
    """Collects failures and return (success, list_of_failures)"""
    failures = list(call())
    return not failures, failures


def has_nans(obj):
    """Check if obj has any NaNs

    Compatible with different behavior of np.isnan, which sometimes applies
    over all axes (py35, py35) and sometimes does not (py34).
    """
    nans = np.isnan(obj)
    while np.ndim(nans):
        nans = np.any(nans)
    return bool(nans)


class DeepcopyMixin:

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

"""Deprecated: DotDict.
"""

class DotDict(dict):
    """We use dot_dict to replace standard Python dictionaries. This is simply
    for the convenience of having dict.property access, instead of the messier
    dict['property'] style.
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

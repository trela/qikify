class dotdict(dict):
    """
    Use dotdict to replace dictionaries. This enables dict.property access.
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

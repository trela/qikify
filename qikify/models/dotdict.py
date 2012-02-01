import collections

class dotdict(dict):
    """We use dotdict to replace standard Python dictionaries. This 
    is simply for the convenience of having dict.property access,
    instead of the messier dict['property'] style.
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


class mdotmap(collections.MutableMapping):
    """We use mdotmap to replace standard Python dictionaries. This 
    is simply for the convenience of having mdotmap.attr access,
    instead of the dict[attr] style.
    
    ** NOT YET WORKING **
    """
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs)) # use the free update to set keys
        
        self.__getattr__= self.__getitem__
        self.__setattr__= self.__setitem__
        self.__delattr__= self.__delitem__
        
    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
from collections import OrderedDict
def toRecursiveDict(obj, classkey=None):
    if isinstance(obj, OrderedDict):
        data = OrderedDict()
        for (k, v) in obj.items():
            data[k] = toRecursiveDict(v, classkey)
        return data
    elif hasattr(obj, '__dict__'):
        data = OrderedDict([(key if not key.startswith('_') else key.replace('_', '', 1), toRecursiveDict(value, classkey))
                     for key, value in obj.__dict__.iteritems()
                     if key == '_name' or not callable(value) and not key.startswith('__')])
        
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    elif hasattr(obj, "_ast"):
        return toRecursiveDict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [toRecursiveDict(v, classkey) for v in obj]
    else:
        return obj

def safeDict(elem, array_of_keys, default=""):
    try:
        for key in array_of_keys:
            elem = elem[key]
        return elem
    except Exception as e:
        return default

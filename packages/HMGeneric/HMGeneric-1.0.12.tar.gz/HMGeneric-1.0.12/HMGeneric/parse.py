def get_object_unbyte(obj):
    '''Returns Unbyted object'''
    if (type(obj) == bytes):
        return bytes(obj).decode()
    else:
        return obj
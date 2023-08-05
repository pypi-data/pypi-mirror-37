
def get_keys(hive , keypath):
    try:
        import winreg
        ob = winreg.OpenKey(hive, keypath, 0, winreg.KEY_READ)
        keys = get_attribs('key', ob)
    except Exception as e:
        print("Exception occured :- {}, key path :- {}".format(e, keypath))
    return keys

def get_values(hive, keypath):
    import winreg
    try:
        with winreg.OpenKey(hive, keypath, 0, winreg.KEY_READ) as subkey:
            v = get_attribs('values',subkey)
    except Exception as e:
        print("Exception occured :- {}, key path :- {}".format(e, keypath))
    return v

def get_attribs(attrib_name, ob):
    import winreg
    count = 0
    attrib = []
    while True:
        try:
            subattribs = winreg.EnumKey(ob, count) if attrib_name is 'key' else winreg.EnumValue(ob, count)
            attrib.append(subattribs)
            count+=1
        except WindowsError as e:
            break
    return attrib

def get_all_values(hive, keypath):
    values = []
    for key in get_keys(hive, keypath):
        for value in get_values(hive, keypath + "\\" + key):
            values.append(value)
    return values

def get_where(values, whereTerm, whereCol = None):
    if(whereCol):
        return [value for value in values if value[whereCol] == whereTerm]
    else:
        return [value for value in values if whereTerm in value]

def get_column(values, col):
    return [value[col] for value in values]

def search_attribute(hive, keypath, attribute):
    for key in get_keys(hive, keypath):
        for value in get_values(hive, keypath + "\\" + key):
            if(attribute in value):
                return {'key':key, 'value':value }
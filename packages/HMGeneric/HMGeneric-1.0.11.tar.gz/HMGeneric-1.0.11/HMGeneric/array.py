def get_phrase_from_list(list, phrase):
    ''' This function return only the objects that has specific phrase '''
    listOut = []
    for obj in list:
        if (phrase in obj):
            listOut.append(obj)
    return listOut

def split_list_by_phrase(list, phrase, location):
    ''' This function split each line in the list and return specififc part of the splitted line '''
    listOut = []
    for line in list:
        listOut.append(str(line).split(phrase)[location])
    return listOut

def count_layers(List):
    ''' This function count the number of dethps of array layers'''
    most = 1
    for e in List:
        if isinstance(e, list):
            count = 1 + count_layers(e)
            if(count > most):
                most = count
    return most
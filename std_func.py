def std_dict_addition(dict, obj):
    if obj in dict:
        dict[obj] += 1
    else:
        dict[obj] = 1
    return dict

def std_return_dict_as_single_string(dict):
    finalString = ""
    for k, v in dict.items():
        finalString += f"{k}:{v}, "
    finalString = finalString[:-2]
    return finalString
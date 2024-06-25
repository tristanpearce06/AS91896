def std_dict_addition(dict, obj):
    if obj in dict:
        dict[obj] += 1
    else:
        dict[obj] = 1
    return dict
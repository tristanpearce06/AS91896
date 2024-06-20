def std_dict_addition(obj):
    dict = {}
    if obj in dict:
        dict[obj] =+ 1
    else:
        dict[obj] = 1
    return dict
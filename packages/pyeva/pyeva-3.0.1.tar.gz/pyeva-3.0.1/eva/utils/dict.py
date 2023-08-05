# pylint: disable=C0103

from collections import namedtuple


def convert_list(_list):
    L = []
    for x in _list:
        if isinstance(x, dict):
            L.append(convert(x))
        elif isinstance(x, (list, tuple)):
            L.append(convert_list(x))
        else:
            L.append(x)
    return L


def convert(dictionary):
    '''(递归)转换字典对象为 namedtuple 对象
    '''

    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = convert(value)
        elif isinstance(value, (list, tuple)):
            dictionary[key] = convert_list(value)

    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


# convert 别名
dict_to_namedtuple = convert


d2n = convert

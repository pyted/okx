import traceback
from copy import deepcopy
from pprint import pprint


def get_short_data(data, length, value_omit='......', key_omit='...', ):
    result_data = data
    if type(data) == list:
        if len(data) > length:
            for i in range(length):
                data[i] = get_short_data(data[i], length)
            result_data = data[0:length] + [value_omit, ]
    elif type(data) == dict:
        if len(data) > length:
            result_data = {}
            for i, (sub_key, sub_value) in enumerate(data.items()):
                if i >= length:
                    break
                sub_value = get_short_data(sub_value, length)
                result_data[sub_key] = sub_value
            result_data[key_omit] = value_omit
    return result_data


def eprint(result, length=5, data_length=30, value_omit='......', key_omit='...', width=120):
    result_copy = deepcopy(result)
    if 'data' in result_copy.keys():
        if type(result_copy['data']) == list:
            short_datas = []
            for data in result['data'][0:data_length]:
                short_data = get_short_data(data, length)
                short_datas.append(short_data)
            if len(result['data']) > data_length:
                short_datas.append(value_omit)

        elif type(result_copy['data']) == dict:
            short_datas = {}
            for i, (key, data) in enumerate(result_copy['data'].items()):
                if i > data_length:
                    break
                short_data = get_short_data(data, length)
                short_datas[key] = short_data

            if len(result['data']) > data_length:
                short_datas[key_omit] = value_omit
        else:
            short_datas = result_copy['data']
        result_copy['data'] = short_datas
    pprint(result_copy, sort_dicts=False, width=width)

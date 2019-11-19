# -*- coding: utf-8 -*-
import json


# from http://blog.csdn.net/duoduo_smile/article/details/52783292
def json_loads(json_text, log_print=False):
    # import yaml
    # return yaml.safe_load(json_text)
    try:
        return _byteify(
            json.loads(json_text, object_hook=_byteify),
            ignore_dicts=True
        )
    except ValueError:
        pass
    # print("json_text[%s] is invalid", json_text) if log_print else None
    return None


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data


def merge(data, new_data):
    if isinstance(data, dict) and isinstance(new_data, dict):
        for key, value in new_data.items():
            if key in data and isinstance(data[key], (list, dict)):
                merge(data[key], value)
            else:
                data[key] = value
    elif isinstance(data, list):
        if isinstance(new_data, list):
            data.extend(new_data)
        elif isinstance(new_data, dict):
            data.extend(new_data.values())
        else:
            data.append(new_data)
    else:
        raise ValueError('Merge [%r] with [%r] failed.' % (data, new_data))

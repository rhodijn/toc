#!/usr/bin/env python3
#
#   ##################      this module keeps track of what happened
#   ##                ##    version 0.3, 2025-05-23
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import datetime, json


def get_value(file, k_1, k_2) -> str:
    """
    check if library parameter is valid

    parameters:
    lib: str = library code

    returns:
    tuple
    """
    try:
        with open(file) as f:
            data = json.load(f)
            return data[k_1][k_2]
    except Exception as e:
        return f'error: {e}'


def json_ld(filename, p) -> dict:
    """
    load json file

    parameters:
    filename: str = library code
    p: str = code for path

    returns:
    log: dict = metadata for current toc
    """
    path = get_value('data/config.json', 'path', p)

    try:
        with open(path + filename, mode='r', encoding='utf-8') as f:
            log = json.load(f)
            return log
    except Exception as e:
        return {}


def json_wr(data, filename, p) -> bool:
    """
    write json file

    parameters:
    d: dict = data to be logged
    filename: str = library code
    p: str = code for path

    returns:
    success: bool = success saving data
    """
    path = get_value('data/config.json', 'path', p)

    try:
        with open(path + filename, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        return False
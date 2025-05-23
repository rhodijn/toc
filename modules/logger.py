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
    try:
        with open(file) as f:
            data = json.load(f)
            return data[k_1][k_2]
    except Exception as e:
        return f'error: {e}'


def json_ld(filename, p) -> dict:
    path = get_value('data/config.json', 'path', p)

    try:
        with open(path + filename, mode='r', encoding='utf-8') as f:
            log = json.load(f)
            return log
    except Exception as e:
        return {}

def json_wr(data, filename, p):
    path = get_value('data/config.json', 'path', p)

    try:
        with open(path + filename, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(data, f, indent=4)
    except Exception as e:
        print(e)
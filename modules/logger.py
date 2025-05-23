#!/usr/bin/env python3

##################      this module keeps track of what happened
##                ##    version 0.1, 2025-05-23
##              ##
  ######      ##
    ##      ######
  ##              ##    created by rhodijn for zhaw hsb
##                ##
  ##################    cc-by-sa [°_°]


import json


def get_value(file, k_1, k_2):
    try:
        with open(file) as f:
            data = json.load(f)
            return data[k_1][k_2]
    except Exception as e:
        return f'error: {e}'
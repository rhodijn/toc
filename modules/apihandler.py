#!/usr/bin/env python3
#
#   ##################      this module communicates with alma
#   ##                ##    version 0.2 (2025-05-23)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import requests

from dotenv import dotenv_values
from logger import *


secrets = dotenv_values('.env')


def api_request(method: str, value: str, param_1: str, param_2='') -> tuple:
    """
    write json file

    parameters:
    method: str = 
    value: str = 
    param_1: str = 
    param_2: str =

    returns:
    response: tuple = request: str, response: requests.models.Response
    """
    config = load_json('config.json', 'd')
    if method == 'get':
        req = f'{secrets["API_URL"]}{param_1}{value}{param_2}&apikey={secrets["API_KEY"]}&format={config["api"]["j"]}'
        response = requests.get(req)
    return req, response
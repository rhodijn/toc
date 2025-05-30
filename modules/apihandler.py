#!/usr/bin/env python3
#
#   ##################      this module communicates with alma
#   ##                ##    version 0.5 (2025-05-27)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    [°_°]
#
#===============================================================================


import requests

from dotenv import dotenv_values
from logger import *


secrets = dotenv_values('.env')


def api_request(method: str, value: str, par_1: str, par_2='') -> tuple:
    """
    write json file

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = 
    param_1: str = 
    param_2: str =

    returns:
    response: tuple = request: str, response: requests.models.Response
    """
    config = load_json('config.json', 'd')

    if method == 'get':
        req = f"{secrets['API_URL']}{par_1}{value}{par_2}&apikey={secrets['API_KEY']}&format={config['api']['j']}"
        response = requests.get(req)

    return req, response


def check_url(processing: dict) -> dict:
    """
    test the link to the pdf

    parameters:
    processing: dict

    returns:
    processing: dict =
    """
    try:
        if processing['url']:
            response = requests.head(processing['url'])

            if response.status_code == 200:
                processing.update({'link_tested': True})
                processing['messages'].append(f"link tested (code: {response.status_code})")
            else:
                processing['messages'].append(f"link test failed (code: {response.status_code})")
        else:
            processing['messages'].append('no url to test')
    except requests.ConnectionError as e:
        processing['messages'].append(f"error: {e} occurred")
    
    return processing